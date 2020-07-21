package com.machine.window;

	import java.awt.Color;
	import java.awt.event.ActionEvent;
	import java.awt.event.MouseEvent;
	import java.awt.event.MouseListener;
import java.io.File;
import java.io.IOException;

import javax.swing.JButton;
	import javax.swing.JLabel;
	import javax.swing.JOptionPane;
	import javax.swing.JPanel;
	import javax.swing.JTextArea;
	import javax.swing.JTextField;

	import com.machine.dataset.Pythondata;
	import com.machine.dataset.Utildata;
	import com.machine.util.Choosefile;

	public class Tree {
	       public JPanel jpanel1 = new JPanel();
	       public JPanel jpanel2 = new JPanel();
	       JTextField trainfiletext = new JTextField();
	       JTextField prefiletext = new JTextField();
	       JTextField outfiletext = new JTextField();
	       JTextField modelfiletext = new JTextField();
	       JTextField splittypetext = new JTextField();
	       JTextArea text = new JTextArea(20,20);
	       public Tree(){
	    	   JLabel label1 = new JLabel();
	    	   JLabel label2 = new JLabel();
	    	   JLabel label3 = new JLabel();
	    	   JLabel label4 = new JLabel();
	    	   JLabel label5 = new JLabel();
	    	   JLabel trainfile = new JLabel();
	    	   JLabel prefile = new JLabel();
	    	   JLabel outfile = new JLabel();
	    	   JLabel modelfile = new JLabel();
	    	   JLabel splittype = new JLabel();
	           JButton train = new JButton();
	           JButton pre = new JButton();
	           JButton out = new JButton();
	           JButton model = new JButton();
	           JButton redo = new JButton();
	           JButton redo1 = new JButton();
	           JButton run = new JButton();
	           JButton run1 = new JButton();
	           
	           label1.setText("*");
	           label1.setForeground(Color.RED);
	           label2.setText("*");
	           label2.setForeground(Color.RED);
	           label3.setText("*");
	           label3.setForeground(Color.RED);
	           label4.setText("*");
	           label4.setForeground(Color.RED);
	           label5.setText("*");
	           label5.setForeground(Color.RED);
	           
	           trainfile.setText("训练数据");
	           prefile.setText("预测数据");
	           outfile.setText("输出数据");
	           modelfile.setText("模型文件");
	           splittype.setText("分 割 符");
	           train.setText("...");
	           pre.setText("...");
	           out.setText("...");
	           model.setText("...");
	           redo.setText("重置");
	           run.setText("确定");
	           run1.setText("确定");
	           redo1.setText("重置");
				text.setFont(new java.awt.Font("微软雅黑", 0, 14));
				text.setBackground(Color.decode("#000080"));
				text.setForeground(Color.RED);
				text.setLineWrap(false);
				trainfiletext.setText("训练数据");
				trainfiletext.setForeground(Color.gray);
				prefiletext.setText("预测数据");
				prefiletext.setForeground(Color.gray);
				outfiletext.setText("输出数据");
				outfiletext.setForeground(Color.gray);
				modelfiletext.setText("模型文件");
				modelfiletext.setForeground(Color.gray);
				splittypetext.setText("分割符");
				splittypetext.setForeground(Color.gray);
				
				trainfiletext.addMouseListener(new MouseListener(){

					@Override
					public void mouseClicked(MouseEvent e) {
						// TODO Auto-generated method stub
						trainfiletext.setText("");
						trainfiletext.setForeground(Color.BLACK);
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
				prefiletext.addMouseListener(new MouseListener(){

					@Override
					public void mouseClicked(MouseEvent e) {
						// TODO Auto-generated method stub
						prefiletext.setText("");
						prefiletext.setForeground(Color.BLACK);
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
				outfiletext.addMouseListener(new MouseListener(){

					@Override
					public void mouseClicked(MouseEvent e) {
						// TODO Auto-generated method stub
						outfiletext.setText("");
						outfiletext.setForeground(Color.BLACK);
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
				modelfiletext.addMouseListener(new MouseListener(){

					@Override
					public void mouseClicked(MouseEvent e) {
						// TODO Auto-generated method stub
						modelfiletext.setText("");
						modelfiletext.setForeground(Color.BLACK);
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
	           train.addActionListener(new java.awt.event.ActionListener(){

				@Override
				public void actionPerformed(ActionEvent e) {
					// TODO Auto-generated method stub
					trainfiletext.setText(Choosefile.choose());
				}
	        	   
	           });
	           pre.addActionListener(new java.awt.event.ActionListener(){

	   			@Override
	   			public void actionPerformed(ActionEvent e) {
	   				// TODO Auto-generated method stub
	   				prefiletext.setText(Choosefile.choose());
	   			}
	           	   
	              });
	           out.addActionListener(new java.awt.event.ActionListener(){

	   			@Override
	   			public void actionPerformed(ActionEvent e) {
	   				// TODO Auto-generated method stub
	   				outfiletext.setText(Choosefile.choose());
	   			}
	           	   
	              });
	           model.addActionListener(new java.awt.event.ActionListener(){

		   			@Override
		   			public void actionPerformed(ActionEvent e) {
		   				// TODO Auto-generated method stub
		   				modelfiletext.setText(Choosefile.choose());
		   			}
		           	   
		              });
	           redo.addActionListener(new java.awt.event.ActionListener(){

	   			@Override
	   			public void actionPerformed(ActionEvent e) {
	   				// TODO Auto-generated method stub
	   				trainfiletext.setText("");
	   				modelfiletext.setText("");
	   				splittypetext.setText("");
	   			}
	           	   
	              });
	           redo1.addActionListener(new java.awt.event.ActionListener(){

	      			@Override
	      			public void actionPerformed(ActionEvent e) {
	      				// TODO Auto-generated method stub
	      				trainfiletext.setText("");
	      				modelfiletext.setText("");
	      				splittypetext.setText("");
	      				prefiletext.setText("");
	      				outfiletext.setText("");
	      			}
	              	   
	                 });
	           
	           run.addActionListener(new java.awt.event.ActionListener(){

	      			@Override
	      			public void actionPerformed(ActionEvent e) {
	      				// TODO Auto-generated method stub
	      				Pythondata.trainfile = trainfiletext.getText();
	      				Pythondata.modelfile = modelfiletext.getText();
	      				Pythondata.splittype = splittypetext.getText();
	      				File file = new File(Pythondata.modelfile);
						if(file.isDirectory()){
						     File newfile = new File(Pythondata.modelfile +"/"+"modelfile");
						     if(newfile.exists()){
						    	 newfile.delete();
						     }
						     try {
								newfile.createNewFile();
							} catch (IOException e1) {
								// TODO Auto-generated catch block
								e1.printStackTrace();
							}
						     Pythondata.modelfile = Pythondata.modelfile + "/" + "modelfile";
						}
						else if(file.isFile()){
							file.delete();
							try {
								file.createNewFile();
							} catch (IOException e1) {
								// TODO Auto-generated catch block
								e1.printStackTrace();
							}
						}
	      				//if(JOptionPane.showConfirmDialog(null, "参数设置成功！","提示",JOptionPane.YES_NO_OPTION)==JOptionPane.YES_OPTION){
						   jpanel1.removeAll();
						   javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(
									jpanel1);
							jpanel1.setLayout(jPanel1Layout);
							jPanel1Layout
									.setHorizontalGroup(jPanel1Layout
											.createParallelGroup(
													javax.swing.GroupLayout.Alignment.LEADING)
											.addGroup(
													//javax.swing.GroupLayout.Alignment.CENTER,
													jPanel1Layout.createSequentialGroup()
													.addContainerGap(1, Short.MAX_VALUE)
													.addComponent(text, 
															javax.swing.GroupLayout.PREFERRED_SIZE, 
															700, 
															javax.swing.GroupLayout.PREFERRED_SIZE)
													.addContainerGap(0, Short.MAX_VALUE)));
							jPanel1Layout
									.setVerticalGroup(jPanel1Layout
											.createParallelGroup(
													javax.swing.GroupLayout.Alignment.LEADING)
											.addGroup(
													jPanel1Layout
															.createSequentialGroup()
															.addGroup(jPanel1Layout
																	.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
																	.addComponent(text))
															.addPreferredGap(
																	javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
															));
				        		 //  }
	      				Utildata.isset = true;}});
	           run1.addActionListener(new java.awt.event.ActionListener(){

	     			@Override
	     			public void actionPerformed(ActionEvent e) {
	     				// TODO Auto-generated method stub
	     				Pythondata.trainfile = trainfiletext.getText();
	     				Pythondata.testfile = prefiletext.getText();
	     				Pythondata.outfile = outfiletext.getText();
	     				Pythondata.modelfile = modelfiletext.getText();
	     				Pythondata.splittype = splittypetext.getText();
	     				//if(JOptionPane.showConfirmDialog(null, "参数设置成功！","提示",JOptionPane.YES_NO_OPTION)==JOptionPane.YES_OPTION){
						   jpanel2.removeAll();
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
				        		   //}
	     				Utildata.isset = true;}});
	           
	           javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(
						jpanel1);
				jpanel1.setLayout(jPanel1Layout);
				jPanel1Layout
						.setHorizontalGroup(jPanel1Layout
								.createParallelGroup(
										javax.swing.GroupLayout.Alignment.LEADING)
								.addGroup(
										//javax.swing.GroupLayout.Alignment.CENTER,
										jPanel1Layout.createSequentialGroup()
										.addContainerGap(280, Short.MAX_VALUE)
										.addComponent(redo, 
												javax.swing.GroupLayout.PREFERRED_SIZE, 
												50, 
												javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(60, Short.MAX_VALUE)
										.addComponent(
												run,
												javax.swing.GroupLayout.PREFERRED_SIZE,
												50,
												javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(280, Short.MAX_VALUE))
								.addGroup(
										//javax.swing.GroupLayout.Alignment.CENTER,
										jPanel1Layout
												.createSequentialGroup()
												.addContainerGap(250, Short.MAX_VALUE)
												.addComponent(label1, 
														javax.swing.GroupLayout.PREFERRED_SIZE, 
														10, 
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(
														splittype,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														50,
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
										jPanel1Layout
												.createSequentialGroup()
												.addContainerGap(250, Short.MAX_VALUE)
												.addComponent(label2,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														10,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(
														modelfile,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														50,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(modelfiletext, 
								                		javax.swing.GroupLayout.PREFERRED_SIZE, 
										                160,
										                javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
								                .addComponent(model,
								                		javax.swing.GroupLayout.PREFERRED_SIZE,
								                		50,
								                		javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(200, Short.MAX_VALUE))
												//.addContainerGap(100, Short.MAX_VALUE))
								.addGroup(
										//javax.swing.GroupLayout.Alignment.CENTER,
										jPanel1Layout.createSequentialGroup()
										.addContainerGap(250, Short.MAX_VALUE)
										.addComponent(label3, 
												javax.swing.GroupLayout.PREFERRED_SIZE, 
												10, 
												javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(1, Short.MAX_VALUE)
										.addComponent(
												trainfile,
												javax.swing.GroupLayout.PREFERRED_SIZE,
												50,
												javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(1, Short.MAX_VALUE)
						                .addComponent(trainfiletext, 
						                		javax.swing.GroupLayout.PREFERRED_SIZE, 
								                160,
								                javax.swing.GroupLayout.PREFERRED_SIZE)
						                .addContainerGap(1, Short.MAX_VALUE)
						                .addComponent(train,
						                		javax.swing.GroupLayout.PREFERRED_SIZE,
						                		50,
						                		javax.swing.GroupLayout.PREFERRED_SIZE)
								.addContainerGap(200, Short.MAX_VALUE))
												);
				jPanel1Layout
						.setVerticalGroup(jPanel1Layout
								.createParallelGroup(
										javax.swing.GroupLayout.Alignment.LEADING)
								.addGroup(
										jPanel1Layout
												.createSequentialGroup()
												.addGroup(jPanel1Layout
														.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
														.addComponent(label3)
														.addComponent(trainfile)
														.addComponent(trainfiletext)
														.addComponent(train))
												.addPreferredGap(
														javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
												.addGroup(
														jPanel1Layout
																.createParallelGroup(
																		javax.swing.GroupLayout.Alignment.BASELINE)
																.addComponent(label2)
																.addComponent(modelfile)
																.addComponent(modelfiletext)
																.addComponent(model)
																)
												.addPreferredGap(
														javax.swing.LayoutStyle.ComponentPlacement.RELATED,
														10, Short.MAX_VALUE)
												.addGroup(jPanel1Layout
														.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
														.addComponent(label1)
														.addComponent(splittype)
														.addComponent(splittypetext))
												.addPreferredGap(
														javax.swing.LayoutStyle.ComponentPlacement.RELATED,
														10, Short.MAX_VALUE)
												.addGroup(jPanel1Layout
														.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
														.addComponent(redo)
														.addComponent(run))
												.addContainerGap()));
	        		   
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
												.addContainerGap(250, Short.MAX_VALUE)
												.addComponent(label1, 
														javax.swing.GroupLayout.PREFERRED_SIZE, 
														10, 
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(
														splittype,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														50,
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
												.addContainerGap(250, Short.MAX_VALUE)
												.addComponent(label2,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														10,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(
														modelfile,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														50,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(modelfiletext, 
								                		javax.swing.GroupLayout.PREFERRED_SIZE, 
										                160,
										                javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
								                .addComponent(model,
								                		javax.swing.GroupLayout.PREFERRED_SIZE,
								                		50,
								                		javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(200, Short.MAX_VALUE))
								.addGroup(
										//javax.swing.GroupLayout.Alignment.CENTER,
										jPanel2Layout
												.createSequentialGroup()
												.addContainerGap(250, Short.MAX_VALUE)
												.addComponent(label3,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														10,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(
														outfile,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														50,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(outfiletext, 
								                		javax.swing.GroupLayout.PREFERRED_SIZE, 
										                160,
										                javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
								                .addComponent(out,
								                		javax.swing.GroupLayout.PREFERRED_SIZE,
								                		50,
								                		javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(200, Short.MAX_VALUE))
								.addGroup(
										//javax.swing.GroupLayout.Alignment.CENTER,
										jPanel2Layout
												.createSequentialGroup()
												.addContainerGap(250, Short.MAX_VALUE)
												.addComponent(label4,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														10,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(
														prefile,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														50,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(prefiletext, 
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
								.addGroup(
										//javax.swing.GroupLayout.Alignment.CENTER,
										jPanel2Layout.createSequentialGroup()
										.addContainerGap(250, Short.MAX_VALUE)
										.addComponent(label5, 
												javax.swing.GroupLayout.PREFERRED_SIZE, 
												10, 
												javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(1, Short.MAX_VALUE)
										.addComponent(
												trainfile,
												javax.swing.GroupLayout.PREFERRED_SIZE,
												50,
												javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(1, Short.MAX_VALUE)
						                .addComponent(trainfiletext, 
						                		javax.swing.GroupLayout.PREFERRED_SIZE, 
								                160,
								                javax.swing.GroupLayout.PREFERRED_SIZE)
						                .addContainerGap(1, Short.MAX_VALUE)
						                .addComponent(train,
						                		javax.swing.GroupLayout.PREFERRED_SIZE,
						                		50,
						                		javax.swing.GroupLayout.PREFERRED_SIZE)
								.addContainerGap(200, Short.MAX_VALUE))
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
														.addComponent(label5)
														.addComponent(trainfile)
														.addComponent(trainfiletext)
														.addComponent(train))
												.addPreferredGap(
														javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
												.addGroup(jPanel2Layout
														.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
														.addComponent(label4)
														.addComponent(prefile)
														.addComponent(prefiletext)
														.addComponent(pre))
												.addPreferredGap(
														javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
												.addGroup(jPanel2Layout
														.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
														.addComponent(label3)
														.addComponent(outfile)
														.addComponent(outfiletext)
														.addComponent(out))
												.addPreferredGap(
														javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
												.addGroup(
														jPanel2Layout
																.createParallelGroup(
																		javax.swing.GroupLayout.Alignment.BASELINE)
																.addComponent(label2)
																.addComponent(modelfile)
																.addComponent(modelfiletext)
																.addComponent(model)
																)
												.addPreferredGap(
														javax.swing.LayoutStyle.ComponentPlacement.RELATED,
														10, Short.MAX_VALUE)
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
}
