package ar.org.hclass;

import java.awt.Canvas;
import java.awt.Dimension;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

import javax.imageio.ImageIO;
import javax.management.RuntimeErrorException;

import org.jmol.adapter.smarter.SmarterJmolAdapter;
import org.jmol.viewer.JmolConstants;
import org.jmol.viewer.Viewer;


public class Pdb2Img {

  
  public static class Result{
    ArrayList<File>  files;
    int processed;


      public Result(ArrayList<File> files, int processed) {
        this.files = files;
        this.processed = processed;
      }

      public ArrayList<File> getFiles() {
        return files;
      }

      public int getProcessed() {
        return processed;
      }

    
  }
    public ArrayList<File> getFiles(String dir) {
      File directory = new File(dir);
      if (!directory.isDirectory()) {
        throw new RuntimeException(" Path " + dir + " is not a directory.");
      }
      ArrayList<File> result = new ArrayList<File>();
      File[] files = directory.listFiles();
      for (File file : files) {
        if (file.isFile()) {
          result.add(file);
        }
      }
      return result;
    }

    public Result generateImages(ArrayList<File> files, String outputPath, boolean force, String format, int width, int height) throws IOException {

      java.awt.Canvas display = new Canvas();
      org.jmol.adapter.smarter.SmarterJmolAdapter adapter = new SmarterJmolAdapter();
      org.jmol.viewer.Viewer viewer = (Viewer) Viewer.allocateViewer(display, adapter, null, null, null, null, null);
      String temporaryOutputFolder= outputPath+"/temporaryProteinImagesGeneration/";
      new File(outputPath).mkdirs();
      new File(temporaryOutputFolder).mkdirs();
      outputPath=new File(outputPath).getAbsolutePath();
      int processed = 0;
      try {
        for (File file : files) {
          //String name = file.getName().split("\\.")[0];
          
          String temporaryOutput = temporaryOutputFolder + file.getName()+ "." + "png";
          String realOutput=  outputPath + "/" + file.getName()+ "." + format;
          if (new File(realOutput).exists() && !force) {
            continue;
          }

          viewer.setScreenDimension(new Dimension(1, 1));
          String path = file.getAbsolutePath();
          viewer.scriptWait("load '" + path + "' {1 1 1};");
          String representation = "set frank off;set defaultStructureDSSP true; zoom 110; set measurementUnits ANGSTROMS; select all; spacefill off; wireframe off; backbone off; cartoon on; color cartoon structure; color structure; select ligand;wireframe 0.16;spacefill 0.5; color cpk ;";
//          String r2 = "select all; model 0;set antialiasDisplay true; ;save STATE state_1;, load '/static/humanpcweb/proteins/d1c0wa3.pdb';; echo;set defaultStructureDSSP true; zoom 110; set measurementUnits ANGSTROMS; select all; spacefill off; wireframe off; backbone off; cartoon on; color cartoon structure; color structure; select ligand;wireframe 0.16;spacefill 0.5; color cpk ; select all; model 0;set antialiasDisplay true;";
          viewer.scriptWait(representation);
          viewer.setScreenDimension(new Dimension(800, 800));
          // anti-aliasing enabled
          viewer.getGraphics3D().setWindowParameters(800, 800, true);

          // Create image

          System.out.println(temporaryOutput);
          viewer.getImageAs("png", 9, width, height, temporaryOutput, null);
          
          this.convertImage(format, temporaryOutput,realOutput);
          
          processed++;
        }
      } finally {
        // Ensure threads are stopped
        viewer.setModeMouse(JmolConstants.MOUSE_NONE);
        new File(temporaryOutputFolder).delete();
      }
      return new Result(files, processed);
    }

    private void convertImage(String format, String temporaryOutput,String realOutput) throws IOException {
    	File file = new File(temporaryOutput);
    	BufferedImage image = ImageIO.read(file);
    	File f = new File(realOutput);
    	ImageIO.write(image, format, f);
    	file.deleteOnExit();

		
	}

	public Result convert(String directoryPath,
            String outputPath, boolean force, String format, int width, int height) throws IOException {
      ArrayList<File> files = getFiles(directoryPath);
      Result result=generateImages(files, outputPath, force, format,width,height);
      return result;

    }

  /**
   * @param args
 * @throws IOException 
   */
  public static void main(String[] args) throws IOException {
     Pdb2Img pdb2Img = new Pdb2Img();

    Pdb2Img.Result result = pdb2Img.convert( "samples",  "samples/images/",  true,  "jpg",800,800);
    System.out.println(" Processed " + result.getProcessed() + " files of " + result.getFiles().size() + ".");
     System.exit(0);
  }
}
