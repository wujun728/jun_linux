package com.machine.window;


	import java.awt.Color;
	import java.awt.event.ActionEvent;
	import java.awt.event.MouseEvent;
	import java.awt.event.MouseListener;

	import javax.swing.JButton;
	import javax.swing.JLabel;
	import javax.swing.JPanel;
	import javax.swing.JTextArea;
	import javax.swing.JTextField;

	import com.machine.dataset.Pythondata;
	import com.machine.dataset.Utildata;
	import com.machine.util.Choosefile;

	public class FP {
	       public JPanel jpanel1 = new JPanel();
	       public JPanel jpanel2 = new JPanel();
	       JTextField minsupporttext = new JTextField();
	       JTextField prefiletext = new JTextField();
	       JTextField outfiletext = new JTextField();
	       JTextField splittypetext = new JTextField();
	       JTextArea text = new JTextArea(20,20);
	       public FP(){
	    	   JLabel label1 = new JLabel();
	    	   JLabel label2 = new JLabel();
	    	   JLabel label3 = new JLabel();
	    	   JLabel label4 = new JLabel();
	    	   JLabel label5 = new JLabel();
	    	   JLabel minsupport = new JLabel();
	    	   JLabel prefile = new JLabel();
	    	   JLabel outfile = new JLabel();
	    	   JLabel minconf = new JLabel();
	    	   JLabel splittype = new JLabel();
	           JButton pre = new JButton();
	           JButton out = new JButton();
	           JButton redo1 = new JButton();
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
	           
	           minsupport.setText("最小支持度");
	           prefile.setText("预测数据");
	           outfile.setText("输出数据");
	           minconf.setText("最小可信度");
	           splittype.setText("分 割 符");
	           pre.setText("...");
	           out.setText("...");
	           run1.setText("确定");
	           redo1.setText("重置");
				text.setFont(new java.awt.Font("微软雅黑", 0, 14));
				text.setBackground(Color.decode("#000080"));
				text.setForeground(Color.RED);
				text.setLineWrap(false);
				minsupporttext.setText("最小支持度（整数）");
				minsupporttext.setForeground(Color.gray);
				prefiletext.setText("预测数据");
				prefiletext.setForeground(Color.gray);
				outfiletext.setText("输出数据");
				outfiletext.setForeground(Color.gray);
				splittypetext.setText("分割符");
				splittypetext.setForeground(Color.gray);
				
				minsupporttext.addMouseListener(new MouseListener(){

					@Override
					public void mouseClicked(MouseEvent e) {
						// TODO Auto-generated method stub
						minsupporttext.setText("");
						minsupporttext.setForeground(Color.BLACK);
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
	          
	           redo1.addActionListener(new java.awt.event.ActionListener(){

	      			@Override
	      			public void actionPerformed(ActionEvent e) {
	      				// TODO Auto-generated method stub
	      				splittypetext.setText("");
	      				prefiletext.setText("");
	      				outfiletext.setText("");
	      			}
	              	   
	                 });
	           
	          
	           run1.addActionListener(new java.awt.event.ActionListener(){

	     			@Override
	     			public void actionPerformed(ActionEvent e) {
	     				// TODO Auto-generated method stub
	     				Pythondata.minsupport = Integer.parseInt(minsupporttext.getText().trim());
	     				Pythondata.testfile = prefiletext.getText();
	     				Pythondata.outfile = outfiletext.getText();
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
												.addContainerGap(240, Short.MAX_VALUE)
												.addComponent(label3,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														10,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(
														outfile,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														60,
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
												.addContainerGap(240, Short.MAX_VALUE)
												.addComponent(label4,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														10,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(
														prefile,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														60,
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
										.addContainerGap(240, Short.MAX_VALUE)
										.addComponent(label5, 
												javax.swing.GroupLayout.PREFERRED_SIZE, 
												10, 
												javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(1, Short.MAX_VALUE)
										.addComponent(
												minsupport,
												javax.swing.GroupLayout.PREFERRED_SIZE,
												60,
												javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(1, Short.MAX_VALUE)
						                .addComponent(minsupporttext, 
						                		javax.swing.GroupLayout.PREFERRED_SIZE, 
								                160,
								                javax.swing.GroupLayout.PREFERRED_SIZE)
						                .addContainerGap(250, Short.MAX_VALUE))
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
														.addComponent(minsupport)
														.addComponent(minsupporttext))
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
