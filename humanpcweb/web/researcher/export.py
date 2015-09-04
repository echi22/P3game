from web.proteins.models import Comparison
from web.proteins.models import ComparisonProtein
from web.researcher.cath_simulator import CathSimulator, Cluster
from web.proteins.game.game_instance_generation import GameInstanceGenerator

def comparison_to_row( comparison, generator,cluster):
    c= comparison
    gi=c.game_instance
    result, different_cath, different_cluster=CathSimulator.game_instance_to_row(gi, generator,cluster)
    protein_window_indexes= map(lambda i: int(i[1])-1,c.order.split("-"))
    protein_window_order= map(lambda i: gi.proteins()[i], protein_window_indexes)
    window= map(lambda p:p.code,protein_window_order)
    type = "estatico" if (c.score.game_type == 1) else "movimiento"
    result=[str(c.user),c.user.userprofile.birthday, c.user.userprofile.knows_proteins,type, c.selected.code,str(c.ts),str(c.accuracy)]+result+window
    return ",".join(map(str,result))

def generate_comparisons_csv():
    
    comparisons=Comparison.objects.order_by('ts')
    header='username,birthday, saw_proteins_before,type, selected,timestamp,accuracy,'+CathSimulator.result_header()+',window_1,window_2,window_3'
    generator = GameInstanceGenerator.get_default_generator()
    cluster= Cluster(Cluster.default_path())
    result= map(lambda c: comparison_to_row(c, generator, cluster), comparisons)
    return  header+ "\n"+ ("\n".join(result))

