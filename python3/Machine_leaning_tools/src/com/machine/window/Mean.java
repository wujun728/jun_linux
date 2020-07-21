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
	public class Mean {
	       public JPanel jpanel2 = new JPanel();
	       JTextField trainfiletext = new JTextField();
	       JTextField numtext = new JTextField();
	       JTextField splittypetext = new JTextField();
	       JTextArea text = new JTextArea(20,20);
	       public Mean(){
	    	   JLabel label1 = new JLabel();
	    	   JLabel label2 = new JLabel();
	    	   JLabel label3 = new JLabel();
	    	   JLabel label4 = new JLabel();
	    	   JLabel label5 = new JLabel();
	    	   JLabel label6 = new JLabel();
	    	   JLabel trainfile = new JLabel();
	    	   JLabel num = new JLabel();
	    	   JLabel splittype = new JLabel();
	           JButton train = new JButton();
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
	           label6.setText("*");
	           label6.setForeground(Color.RED);
	           
	           trainfile.setText("训练数据");
	           num.setText("目标列");
	           splittype.setText("分 割 符");
	           train.setText("...");
	           run1.setText("确定");
	           redo1.setText("重置");
				text.setFont(new java.awt.Font("微软雅黑", 0, 14));
				text.setBackground(Color.decode("#000080"));
				text.setForeground(Color.RED);
				text.setLineWrap(false);
				trainfiletext.setText("训练数据");
				trainfiletext.setForeground(Color.gray);
				numtext.setText("目标列（整数）");
				numtext.setForeground(Color.gray);
				splittypetext.setText("分割符");
				splittypetext.setForeground(Color.gray);
				
				
				numtext.addMouseListener(new MouseListener(){

					@Override
					public void mouseClicked(MouseEvent e) {
						// TODO Auto-generated method stub
						numtext.setText("");
						numtext.setForeground(Color.BLACK);
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
	           
	         
	           redo1.addActionListener(new java.awt.event.ActionListener(){

	      			@Override
	      			public void actionPerformed(ActionEvent e) {
	      				// TODO Auto-generated method stub
	      				trainfiletext.setText("");
	      				numtext.setText("");
	      				splittypetext.setText("");
	      			}
	              	   
	                 });
	           
	          
	           run1.addActionListener(new java.awt.event.ActionListener(){

	     			@Override
	     			public void actionPerformed(ActionEvent e) {
	     				// TODO Auto-generated method stub
	     				Pythondata.trainfile = trainfiletext.getText();
	     				Pythondata.n = Integer.parseInt(numtext.getText().trim());
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
														num,
														javax.swing.GroupLayout.PREFERRED_SIZE,
														50,
														javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(1, Short.MAX_VALUE)
												.addComponent(numtext, 
								                		javax.swing.GroupLayout.PREFERRED_SIZE, 
										                160,
										                javax.swing.GroupLayout.PREFERRED_SIZE)
												.addContainerGap(250, Short.MAX_VALUE))
								.addGroup(
										//javax.swing.GroupLayout.Alignment.CENTER,
										jPanel2Layout.createSequentialGroup()
										.addContainerGap(250, Short.MAX_VALUE)
										.addComponent(label6, 
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
														.addComponent(label6)
														.addComponent(trainfile)
														.addComponent(trainfiletext)
														.addComponent(train))
												.addPreferredGap(
														javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
												.addGroup(
														jPanel2Layout
																.createParallelGroup(
																		javax.swing.GroupLayout.Alignment.BASELINE)
																.addComponent(label2)
																.addComponent(num)
																.addComponent(numtext)
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
