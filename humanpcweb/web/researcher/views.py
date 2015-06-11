
from web.proteins.models import GameInstance, UserProfile, Score, Comparison, GameType
from web.proteins.models import CathClassification
from django.contrib import messages
import logging
import os.path
import tempfile
from zipfile import BadZipfile
from zipfile import ZipFile

from django import forms
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template.context import RequestContext
from django.utils.translation.trans_null import _
from export import generate_comparisons_csv
from web.proteins.models import Classification
from web.proteins.models import Protein
from web import settings
from web.pdb2img import pdb2img
from django.db import transaction
from web.researcher.cath_simulator import CathSimulator
from web.utility import ClassLoader
from web.proteins.game.game_instance_generation import GameInstanceGenerator
logger = logging.getLogger(__name__)

def statistics_by_mission( statistics, generator ):

  csv= "user_level,internal_level,agreement, invalid, wrong, count\n"
  csv+= "\n".join( [ ("%d,%s, %d, %d,%d, %d"  % (i,str (generator.user_level_to_level(i)), s.agreement,s.invalid,s.wrong(),s.count)) for i,s in enumerate(statistics)])
  return csv

class SimulateArtificialPlayers(forms.Form):
  games = forms.IntegerField()

def simulate_cath(request):
  form=SimulateArtificialPlayers(request.GET)
  if not form.is_valid():
      return HttpResponse(status=400)
  games=form.cleaned_data[ "games"]
  generator = GameInstanceGenerator.get_default_generator()
  s=CathSimulator(games)
  print  "Simulating %d games..."  % ( games )
  result,total_cath, total_clusters, statistics_by_game_and_mission, statistics_by_mission_cath,  statistics_by_mission_clusters=s.simulate(generator)
  print  "Simulation finished. Printing Results..."
  csv=  "General Statistics (%d games simulated):\n"  % (games)
  
  csv+=  "\n Cath"+ str(total_cath)
  csv+=  "\n Clusters"+ str(total_clusters)
  csv+=  "\n Cath: statistics for each mission:\n"+ statistics_by_mission(statistics_by_mission_cath, generator)
  csv+=  "\n Clusters: statistics for each mission:\n"+ statistics_by_mission(statistics_by_mission_clusters, generator)
  
  #csv+=  "\nStatistics for each game and mission:\n"
  #csv+= "game, level,agreement, invalid, count\n"
  #csv+= "\n".join( map(lambda s:  "%d, %d, %d, %d, %d"  % (s.game,s.mission,s.statistics.agreement,s.statistics.invalid,s.statistics.count), statistics_by_game_and_mission))
  
  csv+= "\nStatistics for each trio: \n"
  csv+= CathSimulator.result_header()+"\n"
  csv+="\n".join( map(lambda i:  ",".join( map(str,i)),result ))
  response=HttpResponse(csv, mimetype='application/force-download')
  response['Content-Disposition'] = 'attachment; filename=%s' % 'cath-vs-scop.csv'
  return response

class UploadFileForm(forms.Form):

  file = forms.FileField()

  # Almacena en disco el fichero
  # Comprueba que el zip no esta corrupto
  # Devuelve el path absoluto a dicho fichero
  def clean_file(self):
    def ffile_path(uploaded_file):
      '''  Converts InMemoryUploadedFile to on-disk file so it will have path. '''
      try:
        return uploaded_file.temporary_file_path()
      except AttributeError:
        fileno, path = tempfile.mkstemp()
        temp_file = os.fdopen(fileno, 'w+b')
        for chunk in uploaded_file.chunks():
          temp_file.write(chunk)
        temp_file.close()
        return path

    path = ffile_path(self.cleaned_data['file'])
    print path
    print path
    if path==None:
      raise forms.ValidationError('No file selected.')
  
    try: # Comprobacion de que el fichero no esta corrupto
      zf = ZipFile(path)
      bad_file = zf.testzip()
      if bad_file:
        raise forms.ValidationError(_('El fichero "%s" del ZIP esta corrupto.') % bad_file)
      zf.close()
    except BadZipfile:
      raise forms.ValidationError('El fichero subido no es un ZIP.')

    return path

  

    # Ruta donde se encuentra el fichero
		
class UploadClassification(forms.Form):

  file = forms.FileField()

  # Almacena en disco el fichero
  # Devuelve el path absoluto a dicho fichero
  def clean_file(self):
    def ffile_path(uploaded_file):
      '''  Converts InMemoryUploadedFile to on-disk file so it will have path. '''
      try:
        return uploaded_file.temporary_file_path()
      except AttributeError:
        fileno, path = tempfile.mkstemp()
        temp_file = os.fdopen(fileno, 'w+b')
        for chunk in uploaded_file.chunks():
          temp_file.write(chunk)
        temp_file.close()
        return path

    path = ffile_path(self.cleaned_data['file'])
    return path

  def process_file(self):

    # Ruta donde se encuentra el fichero
    filename = self.cleaned_data['file']
    
    f = open(filename, 'r')
    f = list(f)
    print "Processing classification file (%d items)..." % len(f)
    last=""
    try:
      with transaction.commit_on_success():
        for line in f:
          if(last==line):
            print "duplicate - "+line
          if line[0] != '#':
              line = line.split("\n")[0]
              data = line.split(" ")
              scop = data[1].split(".")
              cath = data[3].split(".")
              if (Protein.objects.filter(code=data[0]).count()>1):
                print Protein.objects.filter(code=data[0])
              p = Protein.objects.get(code=data[0])
              s = Classification(protein=p, level1=scop[0], level2=scop[0] + '.' + scop[1], level3=scop[0] + '.' + scop[1] + '.' + scop[2], level4=scop[0] + '.' + scop[1] + '.' + scop[2] + '.' + scop[3])
              s.save()
              c = CathClassification(protein=p, level1=cath[0], level2=cath[0] + '.' + cath[1], level3=cath[0] + '.' + cath[1] + '.' + cath[2], level4=cath[0] + '.' + cath[1] + '.' + cath[2] + '.' + cath[3])
              c.save()
          last=line
    except:
      print line    
    print "Done."       

def regenerate_protein_images(request):
  generate_image_from_proteins(False)
  messages.success(request, "Protein images re-generated")
  return HttpResponseRedirect("/researcher/")

def generate_image_from_proteins(overwrite):
  jar_path = os.path.join(settings.TOOLS_DIR, "pdb2img/pdb2img.jar")
  print "Generating protein images..."
  result_message = pdb2img(settings.PROTEINS_DIR, settings.PROTEIN_IMAGES_DIR, overwrite, settings.PROTEIN_IMAGES_FORMAT, jar_path, settings.PROTEIN_IMAGES_SIZE)
  print "Done. (%s)" % result_message
  print "Generating protein thumbnails..."
  result_message = pdb2img(settings.PROTEINS_DIR, settings.PROTEIN_THUMBNAILS_DIR, overwrite, settings.PROTEIN_THUMBNAILS_FORMAT, jar_path, settings.PROTEIN_THUMBNAILS_SIZE)
  print "Done. (%s)" % result_message


def upload_proteins(request):
  if request.method == 'POST':

    form = UploadFileForm(request.POST, request.FILES)

    # Si el formulario el valido, proceso el fichero
    if form.is_valid():
#
      zipdata = request.FILES['file']
      title = request.FILES['file'].name
      try:
        path = form.cleaned_data['file']
        listado = process_zip(path)
        print listado
        
        messages.success(request, " Proteins successfully uploaded. ")
      except Exception as e:
        print  "error uploading protein file"+str(e)
        messages.error(request, "File %s is not a valid zip or contains errors" % (path))
    else:
      messages.error(request, "The file could not be uploaded.")
  else:
    form = UploadFileForm()
  c = {'form':form}
  c.update(csrf(request))
  return render_to_response('researcher/upload_proteins.html', c, context_instance=RequestContext(request))

def upload_classification(request):
  if request.method == 'POST':

    form = UploadClassification(request.POST, request.FILES)

    # Si el formulario el valido, proceso el fichero
    if form.is_valid():
      form.process_file()
      messages.success(request, "Protein classification successfully uploaded ")
    else:
      messages.error(request, "Could not upload classification. ")
  else:
    form = UploadClassification()
  c = {'form':form}
  c.update(csrf(request))
  return render_to_response('researcher/upload_classification.html', c, context_instance=RequestContext(request))


def index(request):
  return render_to_response('researcher/index.html', context_instance=RequestContext(request))

def download_comparisons(request):
  if request.method == 'GET':
    response = HttpResponse(generate_comparisons_csv(), mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % 'classification.csv'
    return response

def load_proteins_from_server(request):
  if request.method == 'POST':
    path = settings.PROTEINS_MANUAL_UPLOAD_PATH
    if (os.path.exists(path)):
      try:
        process_zip(path)
        messages.success(request, " Proteins successfully uploaded. ")
      except:
        messages.error(request, "File %s is not a valid zip or contains errors" % (path))
    else:
      message = "No file was found in path:  %s" % (path)
      messages.error(request, message)
  return HttpResponseRedirect("/researcher/")

def process_zip(zip_filepath):
  # Lugar donde se alojaran los ficheros descomprimidos
  dirname = settings.PROTEINS_DIR
  if not (os.path.exists(dirname)):
    os.mkdir(settings.PROTEINS_DIR)

  zip = ZipFile(zip_filepath)

  lista_ficheros = []
  # Recorremos todos los ficheros que contiene el zip
  for filepath in zip.namelist():
    filename = os.path.basename(filepath)
    print filename
    target_filepath = os.path.join(dirname, filename)
    code = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    # Si es un directorio, lo creamos
    if not os.path.isdir(filepath):
      if(extension in settings.VALID_PROTEIN_EXTENSIONS):
        outfile = open(target_filepath, 'wb')
        outfile.write(zip.read(filepath))
        outfile.close()
        lista_ficheros.append(target_filepath)
        p = Protein(name=filename, code=code, description='')
        p.save();

  zip.close()
  #os.unlink(zip_filename)
  #generate_image_from_proteins(False)
  return lista_ficheros


def do_clear_game_instances():
    while GameInstance.objects.all().count() > 0:
        q = GameInstance.objects.all().values('id')[:999]
        GameInstance.objects.filter(id__in=q).delete()

def do_clear_scores():    
    while Score.objects.all().count() > 0:
        q = Score.objects.all().values('id')[:999]
        Score.objects.filter(id__in=q).delete()       
    reset_users_profile()
    
def reset_users_profile():
    for user in UserProfile.objects.all():
        user.reset_score()
        
def clear_scores(request):
    do_clear_scores()
    messages.success(request, 'Scores cleared.')
    return HttpResponseRedirect("/researcher/")

def clear_game_instances(request):
    do_clear_scores()
    do_clear_game_instances()
    messages.success(request, 'Game instances cleared.')
    return HttpResponseRedirect("/researcher/")
          
def clear_proteins(request):
  clear_all(Protein)
  messages.success(request, 'Proteins cleared.')
  return HttpResponseRedirect("/researcher/")
def clear_classification(request):
  clear_all(Classification)
  clear_all(CathClassification)
  messages.success(request, 'Classification cleared.')
  return HttpResponseRedirect("/researcher/")

def clear_all(model):
      while model.objects.all().count() > 0:
        q = model.objects.all().values('id')[:999]
        model.objects.filter(id__in=q).delete()   

class ChooseTypeForm(forms.Form):
  game_type = forms.CharField(max_length=100)
def update_corrects(request):
  form = ChooseTypeForm(request.GET)
  if form.is_valid():
    game_type = form.cleaned_data["game_type"]
    if game_type == "movies":
      game_type_enum = GameType.movies
    else:
      game_type_enum = GameType.static
    for gi in GameInstance.objects.filter(times_played__gte=1):
      votes = gi.get_votes_update(game_type_enum)
      max_votes = max(votes)
      if max_votes != 0:
        positions = [i for i, j in enumerate(votes) if j == max_votes]
        print "------------------------"
        print game_type
        print " votos: "
        print votes
        print gi.proteins()[0].id
        print gi.proteins()[1].id
        print gi.proteins()[2].id
        print " pero wins: "
        print gi.proteins()[positions[0]].id
        print " antes movies: "
        print gi.different_movies.id
        print " antes static: "
        print gi.different_static.id
        print "------------------------"
        if (game_type_enum == GameType.static):
          gi.different_static = gi.proteins()[positions[0]]
        elif (game_type_enum == GameType.movies):
          gi.different_movies = gi.proteins()[positions[0]]
        gi.save()
    return HttpResponseRedirect("/researcher/")
  else:
    return HttpResponseRedirect('/')
  