package pdb2img;

import ar.org.hclass.Pdb2Img;
import java.io.File;
import java.io.IOException;
import java.util.Iterator;

import javax.imageio.ImageIO;
import javax.imageio.ImageWriter;

/**
 *
 * @author facundoq
 */
public class Main {

  public static void help() {
    System.err.println("The source folder must contain just protein files.\n Arguments: sourceDirectoryPath outputDirectoryPath overwrite(true, false) outputFormat(png, jpg) size(WidthxHeight)");
  }

  public static class Arguments{
	  boolean overwrite;
	  String inputFolder,outputPath,format;
	  int width, height;
	public Arguments(boolean overwrite, String inputFolder, String outputPath,
			String format, int width, int height) {
		super();
		this.overwrite = overwrite;
		this.inputFolder = inputFolder;
		this.outputPath = outputPath;
		this.format = format;
		this.width = width;
		this.height = height;
	}
	public boolean isOverwrite() {
		return overwrite;
	}
	public String getInputFolder() {
		return inputFolder;
	}
	public String getOutputPath() {
		return outputPath;
	}
	public String getFormat() {
		return format;
	}
	public int getWidth() {
		return width;
	}
	public int getHeight() {
		return height;
	}
	
  }
  
  
  public static Arguments parseArguments(String[] arguments){
	  if (arguments.length != 5) {
	      System.err.println("wrong number of arguments: " + arguments.length+  ", arguments: "+arguments.toString());
	      help();
	      System.exit(1);
	    }
	    boolean overwrite = false;
	    if (arguments[2].equalsIgnoreCase("true")) {
	      overwrite = true;
	    } else if (!arguments[2].equalsIgnoreCase("false")) {
	      System.err.println("wrong value for overwrite: " + arguments[3]);
	      help();
	      System.exit(2);
	    }
	    String directoryPath = arguments[0];
	    if (! (new File(directoryPath).exists() && new File(directoryPath).isDirectory())) {
	      System.err.println("source directory path does not exist or is not a directory: ("+ directoryPath+ ") ");
	      help();
	      System.exit(3);
	    }

	    String outputPath = arguments[1];
	    String format = arguments[3];
	    Iterator<ImageWriter> imageWritersByFormatName = ImageIO.getImageWritersByFormatName(format);
	    if (!imageWritersByFormatName.hasNext()) {
	      System.err.println("unsupported image format " + format);
	      help();
	      System.exit(4);
	    }
	    
	    String[] size = arguments[4].split("x");
	    
	    if (size.length!=2) {
	      System.err.println("wrong size: " + arguments[4]);
	      help();
	      System.exit(5);
	    }
	    int width=100;
	    int height=100;
	    try{
	    	width= Integer.parseInt(size[0]);
	        height= Integer.parseInt(size[1]);
	    }catch (NumberFormatException e) {
	        System.err.println("wrong size: " + arguments[4]);
	        help();
	        System.exit(6);
		}
	    return new Arguments(overwrite, directoryPath, outputPath, format, width, height);

  }
  /**
   * @param arguments the command line arguments
   */
  public static void main(String[] arguments) {
	  
    Arguments a=parseArguments(arguments);    
    Pdb2Img pdb2Img = new Pdb2Img();
    
    Pdb2Img.Result result;
    
    System.out.println("starting processing of images:");
	try {
		result = pdb2Img.convert(a.getInputFolder(), a.getOutputPath(), a.isOverwrite(),a.getFormat(),a.getWidth(),a.getHeight());
	    System.out.println(" Processed " + result.getProcessed() + " files of " + result.getFiles().size() + ".");
	} catch (IOException e) {
		System.out.println("Cannot convert images to format: "+a.getFormat()+ " ("+e.getLocalizedMessage()+ ").");
		System.exit(1);
	}
     System.exit(0);
  }
}

