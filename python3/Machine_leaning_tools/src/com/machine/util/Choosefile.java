package com.machine.util;


	import java.io.File;

	import javax.swing.JFileChooser;
	import javax.swing.JLabel;

	public class Choosefile{

		public static String choose(){
			// TODO Auto-generated method stub
			JFileChooser jfc=new JFileChooser();
			jfc.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES );
			jfc.showDialog(new JLabel(), "文件");
			File file=jfc.getSelectedFile();
			return file.getAbsolutePath();		
		}
}
