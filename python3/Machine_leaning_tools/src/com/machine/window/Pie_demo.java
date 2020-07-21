package com.machine.window;

	import java.awt.Color;
	import java.awt.event.ActionEvent;
	import java.awt.event.MouseEvent;
	import java.awt.event.MouseListener;
	import java.io.File;
	import java.io.IOException;
	import java.net.URL;

	import javax.swing.JButton;
	import javax.swing.JLabel;
	import javax.swing.JPanel;
	import javax.swing.JTextArea;
	import javax.swing.JTextField;

	import com.machine.dataset.Drewdata;
	import com.machine.dataset.Utildata;
	import com.machine.util.Choosefile;

	public class Pie_demo {
	       public JPanel jpanel1 = new JPanel();
	       public JPanel jpanel2 = new JPanel();
	       JTextField xlabeltext = new JTextField();
	       JTextField drewfiletext = new JTextField();
	       JTextField rangetext = new JTextField();
	       JTextField splittypetext = new JTextField();
	       JTextArea text = new JTextArea(20,20);
	       public Pie_demo(){
	    	   JLabel label1 = new JLabel();
	    	   JLabel label4 = new JLabel();
	    	   JLabel label5 = new JLabel();
	    	   JLabel xlabel = new JLabel();
	    	   JLabel drewfile = new JLabel();
	    	   JLabel range = new JLabel();
	    	   JLabel splittype = new JLabel();
	           JButton pre = new JButton();
	           JButton redo1 = new JButton();
	           JButton run1 = new JButton();
	           
	           label1.setText("*");
	           label1.setForeground(Color.RED);
	           label4.setText("*");
	           label4.setForeground(Color.RED);
	           label5.setText("*");
	           label5.setForeground(Color.RED);
	           
	           xlabel.setText("目标列");
	           drewfile.setText("绘图文件");
	           range.setText("取值范围");
	           splittype.setText("分 割 符");
	           pre.setText("...");
	           run1.setText("绘图");
	           redo1.setText("重置");
				text.setFont(new java.awt.Font("微软雅黑", 0, 14));
				text.setBackground(Color.decode("#000080"));
				text.setForeground(Color.RED);
				text.setLineWrap(false);
				xlabeltext.setText("目标列");
				xlabeltext.setForeground(Color.gray);
				drewfiletext.setText("绘图文件");
				drewfiletext.setForeground(Color.gray);
				rangetext.setText("用逗号分割（5,10,15)");
				rangetext.setForeground(Color.gray);
				splittypetext.setText("分割符");
				splittypetext.setForeground(Color.gray);
				
				xlabeltext.addMouseListener(new MouseListener(){

					@Override
					public void mouseClicked(MouseEvent e) {
						// TODO Auto-generated method stub
						xlabeltext.setText("");
						xlabeltext.setForeground(Color.BLACK);
					}

					@Override
					public void mousePressed(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}

					@Override
					public void mouseReleased(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}

					@Override
					public void mouseEntered(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}

					@Override
					public void mouseExited(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}
					
				});
				drewfiletext.addMouseListener(new MouseListener(){

					@Override
					public void mouseClicked(MouseEvent e) {
						// TODO Auto-generated method stub
						drewfiletext.setText("");
						drewfiletext.setForeground(Color.BLACK);
					}

					@Override
					public void mousePressed(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}

					@Override
					public void mouseReleased(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}

					@Override
					public void mouseEntered(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}

					@Override
					public void mouseExited(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}
					
				});
				rangetext.addMouseListener(new MouseListener(){

					@Override
					public void mouseClicked(MouseEvent e) {
						// TODO Auto-generated method stub
						rangetext.setText("");
						rangetext.setForeground(Color.BLACK);
					}

					@Override
					public void mousePressed(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}

					@Override
					public void mouseReleased(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}

					@Override
					public void mouseEntered(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}

					@Override
					public void mouseExited(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}
					
				});
				splittypetext.addMouseListener(new MouseListener(){

					@Override
					public void mouseClicked(MouseEvent e) {
						// TODO Auto-generated method stub
						splittypetext.setText("");
						splittypetext.setForeground(Color.BLACK);
					}

					@Override
					public void mousePressed(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}

					@Override
					public void mouseReleased(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}

					@Override
					public void mouseEntered(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}

					@Override
					public void mouseExited(MouseEvent e) {
						// TODO Auto-generated method stub
						
					}
					
				});
	           pre.addActionListener(new java.awt.event.ActionListener(){

	   			@Override
	   			public void actionPerformed(ActionEvent e) {
	   				// TODO Auto-generated method stub
	   				drewfiletext.setText(Choosefile.choose());
	   			}
	           	   
	              });
	          
	           redo1.addActionListener(new java.awt.event.ActionListener(){

	      			@Override
	      			public void actionPerformed(ActionEvent e) {
	      				// TODO Auto-generated method stub
	      				splittypetext.setText("");
	      				drewfiletext.setText("");
	      				rangetext.setText("");
	      				xlabeltext.setText("");
	      			}
	              	   
	                 });
	          
	           run1.addActionListener(new java.awt.event.ActionListener(){

	     			@Override
	     			public void actionPerformed(ActionEvent e) {
	     				// TODO Auto-generated method stub
	     				Drewdata.x = Integer.parseInt(xlabeltext.getText().trim());
	     				Drewdata.drewfile = drewfiletext.getText();
	     				System.out.println(rangetext.getText());
	     				if(!rangetext.getText().equals("") && !"用逗号分割（5,10,15)".equals(rangetext.getText())){
	     				Drewdata.range = rangetext.getText();
	     				}
	     				Drewdata.splittype = splittypetext.getText();
						   jpanel2.removeAll();
						   javax.swing.GroupLayout jPanel2Layout = new javax.swing.GroupLayout(
									jpanel2);
							jpanel2.setLayout(jPanel2Layout);
							jPanel2Layout
									.setHorizontalGroup(jPanel2Layout
											.createParallelGroup(
													javax.swing.GroupLayout.Alignment.LEADING)
											.addGroup(
													jPanel2Layout.createSequentialGroup()
													.addContainerGap(1, Short.MAX_VALUE)
													.addComponent(text, 
															javax.swing.GroupLayout.PREFERRED_SIZE, 
															700, 
															javax.swing.GroupLayout.PREFERRED_SIZE)
													.addContainerGap(0, Short.MAX_VALUE)));
							jPanel2Layout
									.setVerticalGroup(jPanel2Layout
											.createParallelGroup(
													javax.swing.GroupLayout.Alignment.LEADING)
											.addGroup(
													jPanel2Layout
															.createSequentialGroup()
															.addGroup(jPanel2Layout
																	.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
																	.addComponent(text))
															.addPreferredGap(
																	javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
															));
	     				drew();}});
	        		   
				javax.swing.GroupLayout jPanel2Layout = new javax.swing.GroupLayout(
						jpanel2);
				jpanel2.setLayout(jPanel2Layout);
				jPanel2Layout
						.setHorizontalGroup(jPanel2Layout
								.createParallelGroup(
										javax.swing.GroupLayout.Alignment.LEADING)
								.addGroup(
										//javax.swing.GroupLayout.Alignment.CENTER,
										jPanel2Layout.createSequentialGroup()
										.addContainerGap(280, Short.MAX_VALUE)
										.addComponent(redo1, 
												javax.swing.GroupLayout.PREFERRED_SIZE, 
												50, 
												javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(60, Short.MAX_VALUE)
										.addComponent(
												run1,
												javax.swing.GroupLayout.PREFERRED_SIZE,
												50,
												javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(280, Short.MAX_VALUE))
								.addGroup(
										//javax.swing.GroupLayout.Alignment.CENTER,
										jPanel2Layout
												.createSequentialGroup()
												.addContainerGap(240, Short.MAX_VALUE)
												.addComponent(label1, 
														javax.swing.GroupLayout.PREFERRED_SIZE, 
														10, 
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(
														splittype,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														60,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
								                .addComponent(splittypetext, 
								                		javax.swing.GroupLayout.PREFERRED_SIZE, 
										                160,
										                javax.swing.GroupLayout.PREFERRED_SIZE)
								                .addContainerGap(250, Short.MAX_VALUE)
								                )
								.addGroup(
										//javax.swing.GroupLayout.Alignment.CENTER,
										jPanel2Layout
												.createSequentialGroup()
												.addContainerGap(244, Short.MAX_VALUE)
												.addComponent(
														range,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														60,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(rangetext, 
								                		javax.swing.GroupLayout.PREFERRED_SIZE, 
										                160,
										                javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(246, Short.MAX_VALUE))
								.addGroup(
										//javax.swing.GroupLayout.Alignment.CENTER,
										jPanel2Layout.createSequentialGroup()
										.addContainerGap(240, Short.MAX_VALUE)
										.addComponent(label5, 
												javax.swing.GroupLayout.PREFERRED_SIZE, 
												10, 
												javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(1, Short.MAX_VALUE)
										.addComponent(
												xlabel,
												javax.swing.GroupLayout.PREFERRED_SIZE,
												60,
												javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(1, Short.MAX_VALUE)
						                .addComponent(xlabeltext, 
						                		javax.swing.GroupLayout.PREFERRED_SIZE, 
								                160,
								                javax.swing.GroupLayout.PREFERRED_SIZE)
						                .addContainerGap(250, Short.MAX_VALUE))
								.addGroup(
										//javax.swing.GroupLayout.Alignment.CENTER,
										jPanel2Layout
												.createSequentialGroup()
												.addContainerGap(240, Short.MAX_VALUE)
												.addComponent(label4,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														10,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(
														drewfile,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														60,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(drewfiletext, 
								                		javax.swing.GroupLayout.PREFERRED_SIZE, 
										                160,
										                javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
								                .addComponent(pre,
								                		javax.swing.GroupLayout.PREFERRED_SIZE,
								                		50,
								                		javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(200, Short.MAX_VALUE))
												//.addContainerGap(100, Short.MAX_VALUE))
												);
				jPanel2Layout
						.setVerticalGroup(jPanel2Layout
								.createParallelGroup(
										javax.swing.GroupLayout.Alignment.LEADING)
								.addGroup(
										jPanel2Layout
												.createSequentialGroup()
												.addGroup(jPanel2Layout
														.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
														.addComponent(label4)
														.addComponent(drewfile)
														.addComponent(drewfiletext)
														.addComponent(pre))
												.addPreferredGap(
														javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
												.addGroup(jPanel2Layout
														.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
														.addComponent(label5)
														.addComponent(xlabel)
														.addComponent(xlabeltext))
												.addPreferredGap(
														javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
												.addGroup(jPanel2Layout
														.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
														.addComponent(range)
														.addComponent(rangetext))
												.addPreferredGap(
														javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
												.addGroup(jPanel2Layout
														.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
														.addComponent(label1)
														.addComponent(splittype)
														.addComponent(splittypetext))
												.addPreferredGap(
														javax.swing.LayoutStyle.ComponentPlacement.RELATED,
														10, Short.MAX_VALUE)
												.addGroup(jPanel2Layout
														.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
														.addComponent(redo1)
														.addComponent(run1))
												.addContainerGap()));
	           
	       }
		private void drew() {
			// TODO Auto-generated method stub
				String[] pie_demo = {"python","pie_demo2.py",Drewdata.drewfile,String.valueOf(Drewdata.x),
						Drewdata.range,Drewdata.splittype};
						ProcessBuilder processBuilder = new ProcessBuilder();
						URL str = this.getClass().getClassLoader().getResource("com/machine/drew");
						processBuilder.command(pie_demo);  
						processBuilder.directory(new File(str.getPath()));//切换工作目录 
						processBuilder.redirectErrorStream(true);  
						try {
							java.lang.Process process = processBuilder.start();
						} catch (IOException e1) {
							// TODO Auto-generated catch block
							e1.printStackTrace();
						}
			     				
		}
}
