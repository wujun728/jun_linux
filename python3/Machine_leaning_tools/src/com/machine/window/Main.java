package com.machine.window;
	/*
	 * Login.java
	 *
	 * Created on __DATE__, __TIME__
	 */

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.Image;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

import com.machine.util.Choosepython;
import com.machine.util.DateUtil;
import com.machine.dataset.Pythondata;
import com.machine.dataset.Utildata;
		/**
		 *
		 * @author  __USER__
		 */
			public class Main extends javax.swing.JFrame {

				/**
				 * 
				 */
				private static final long serialVersionUID = 907406449685862563L;
				boolean run = false;

				/** Creates new form Main */
				int value = 0;
				public Main() {				
					super("Library Manager System");	
					Image ime = new ImageIcon(this.getClass().getClassLoader().getResource("com/images/ico.png")).getImage();
					setIconImage(ime);
					initComponents();
					setLocationRelativeTo(null);
					this.setResizable(false);
				}

				//GEN-BEGIN:initComponents
				// <editor-fold defaultstate="collapsed" desc="Generated Code">
				@SuppressWarnings("unchecked")
				private void initComponents() {

					jPanel1 = new javax.swing.JPanel();
					new javax.swing.JLabel();
					end_time = new javax.swing.JLabel();
					start_time = new javax.swing.JLabel();
					nend_time = new javax.swing.JLabel();
					nstart_time = new javax.swing.JLabel();
					main_time = new javax.swing.JLabel();
					main_status = new javax.swing.JPanel();
					status = new javax.swing.JProgressBar();
					new javax.swing.JLabel();
					jMenuBar1 = new javax.swing.JMenuBar();
					drew_lifang = new javax.swing.JMenu();
					bar_demo = new javax.swing.JMenuItem();
					bar_barh = new javax.swing.JMenuItem();
					bar_polar = new javax.swing.JMenuItem();
					drew_crcle = new javax.swing.JMenu();
					pie_demo = new javax.swing.JMenuItem();
					jMenuItem11 = new javax.swing.JMenuItem();
					jMenu8 = new javax.swing.JMenu();
					drew_point = new javax.swing.JMenu();
					point_polar = new javax.swing.JMenuItem();
					point_3D = new javax.swing.JMenuItem();
					point_legend = new javax.swing.JMenuItem();
					point_demo = new javax.swing.JMenuItem();
					point_hist = new javax.swing.JMenuItem();
					drew_line = new javax.swing.JMenu();
					line_demo = new javax.swing.JMenuItem();
					line_dash = new javax.swing.JMenuItem();
					line_3D = new javax.swing.JMenuItem();
					jMenu3 = new javax.swing.JMenu();
					jMenu10 = new javax.swing.JMenu();
					jMenuItem21 = new javax.swing.JMenuItem();
					jMenuItem23 = new javax.swing.JMenuItem();
					jMenu4 = new javax.swing.JMenu();
					jMenuItem17 = new javax.swing.JMenuItem();
					jMenuItem18 = new javax.swing.JMenuItem();
					jPanel4 = new javax.swing.JPanel();
					jPanel3 = new javax.swing.JPanel();
					jPanel2 = new javax.swing.JPanel();
					jPanel5 = new javax.swing.JPanel();
					new javax.swing.JPanel();
					new javax.swing.JPanel();
					 text = new JTextArea(20,20);
					 comp = new JProgressBar();
					 lei = new JComboBox<Object>(Utildata.type);
					 suanfa = new JComboBox<String>(Utildata.label1);
					 rolltext = new JScrollPane(text);
					 testbutton = new JButton();
					 trainbutton = new JButton();
					 prebutton = new JButton();
					 runtext = new JTextArea(1,20);
					

					setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
					setTitle("Library Manager System");
					
					//main_img.setIcon(new javax.swing.ImageIcon(
							//this.getClass().getClassLoader().getResource("com/images/main_3.jpg"))); // NOI18N
					jPanel1.setLayout(new GridLayout(3,1,5,5));
					jPanel2.setLayout(new GridLayout(1,1));
					jPanel3.setLayout(new GridLayout(1,3,4,4));
					jPanel4.setLayout(new GridLayout(1,1));
					jPanel5.setLayout(new GridLayout(1,1));
					jPanel5.setBackground(Color.WHITE);

					//jPanel2.setSize(100, 10);
					runtext.setEditable(false);
					runtext.setForeground(Color.RED);
					runtext.setFont(new java.awt.Font("微软雅黑", 0, 35));
					runtext.setBackground(Color.blue);
					text.setEditable(false);
					text.setFont(new java.awt.Font("微软雅黑", 0, 14));
					text.setBackground(Color.decode("#000080"));
					text.setForeground(Color.RED);
					text.setLineWrap(false);
					comp.setSize(100, 10);
					comp.setForeground(Color.CYAN);
					comp.setBackground(Color.blue);
					comp.setPreferredSize(new Dimension(700,40));
					testbutton.setText("测试数据");
					testbutton.setBackground(Color.CYAN);
					trainbutton.setText("训练数据");
					trainbutton.setBackground(Color.CYAN);
					prebutton.setText("参数设置");
					prebutton.setBackground(Color.CYAN);
					lei.setPreferredSize(new Dimension(140,10));
					suanfa.setPreferredSize(new Dimension(140,10));
					//jPanel4.setBackground(Color.BLUE);
					//prebutton.setBounds(20, 20, 50, 20);
		
					jPanel2.add(runtext);
					jPanel2.setVisible(true);
					
					jPanel5.add(prebutton,BorderLayout.CENTER );
					
					jPanel4.add(rolltext);

					//jPanel3.setSize(300, 40);
					jPanel3.add(lei);
					jPanel3.add(suanfa);
					//jPanel3.add(jPanel5);


					main_time.setFont(new java.awt.Font("微软雅黑", 0, 12));
					main_time.setForeground(new java.awt.Color(102, 102, 102));
					main_time.setText("time");
					
					start_time.setFont(new java.awt.Font("微软雅黑",0,12));
					start_time.setForeground(new java.awt.Color(102, 102, 102));
					start_time.setText("开始时间>>");
					
					end_time.setFont(new java.awt.Font("微软雅黑",0,12));
					end_time.setForeground(new java.awt.Color(102, 102, 102));
					end_time.setText("结束时间>>");
					
					nstart_time.setFont(new java.awt.Font("微软雅黑",0,12));
					nstart_time.setForeground(new java.awt.Color(102, 102, 102));
					//nstart_time.setText("开始时间>>");
					
					nend_time.setFont(new java.awt.Font("微软雅黑",0,12));
					nend_time.setForeground(new java.awt.Color(102, 102, 102));
					//nend_time.setText("结束时间>>");
					
					javax.swing.GroupLayout jPanel5Layout = new javax.swing.GroupLayout(jPanel5);
					jPanel5.setLayout(jPanel5Layout);
					jPanel5Layout
					        .setHorizontalGroup(jPanel5Layout
							.createParallelGroup(
									javax.swing.GroupLayout.Alignment.LEADING)
							.addGroup(
									javax.swing.GroupLayout.Alignment.TRAILING,
									jPanel5Layout
											.createSequentialGroup()
											.addContainerGap(100, Short.MAX_VALUE)
											.addComponent(
													prebutton,
													javax.swing.GroupLayout.PREFERRED_SIZE,
													100,
													javax.swing.GroupLayout.PREFERRED_SIZE)
											.addContainerGap(100,Short.MAX_VALUE)
											));
					
					jPanel5Layout
					.setVerticalGroup(jPanel5Layout
							.createParallelGroup(
									javax.swing.GroupLayout.Alignment.LEADING)
							.addGroup(
													jPanel5Layout
															.createParallelGroup(
																	javax.swing.GroupLayout.Alignment.CENTER)
															.addComponent(
																	prebutton,
																	javax.swing.GroupLayout.DEFAULT_SIZE,
																	17,
																	Short.MAX_VALUE)
															.addGap(0,0,0)));
					
					
					javax.swing.GroupLayout jPanel1Layout = new javax.swing.GroupLayout(
							jPanel1);
					jPanel1.setLayout(jPanel1Layout);
					jPanel1Layout
							.setHorizontalGroup(jPanel1Layout
									.createParallelGroup(
											javax.swing.GroupLayout.Alignment.LEADING)
									.addGroup(
											javax.swing.GroupLayout.Alignment.CENTER,
											jPanel1Layout
													.createSequentialGroup()
													.addComponent(
															jPanel4,
															javax.swing.GroupLayout.PREFERRED_SIZE,
															700,
															javax.swing.GroupLayout.PREFERRED_SIZE)
													)
									.addGroup(
											javax.swing.GroupLayout.Alignment.CENTER,
											jPanel1Layout
													.createSequentialGroup()
													.addContainerGap(0, Short.MAX_VALUE)
													.addComponent(jPanel3,javax.swing.GroupLayout.PREFERRED_SIZE,
															300,
															javax.swing.GroupLayout.PREFERRED_SIZE)
													.addContainerGap(10, Short.MAX_VALUE)
													.addPreferredGap(
															javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
													.addComponent(
															jPanel5,
															javax.swing.GroupLayout.PREFERRED_SIZE,
															370,
															javax.swing.GroupLayout.PREFERRED_SIZE)
													.addContainerGap(0, Short.MAX_VALUE))
									.addGroup(
											jPanel1Layout.createSequentialGroup()
													.addComponent(jPanel2,javax.swing.GroupLayout.PREFERRED_SIZE,
															700,
															javax.swing.GroupLayout.PREFERRED_SIZE)
													));
					jPanel1Layout
							.setVerticalGroup(jPanel1Layout
									.createParallelGroup(
											javax.swing.GroupLayout.Alignment.LEADING)
									.addGroup(
											jPanel1Layout
													.createSequentialGroup()
													.addGap(10, 10, 10)
													.addComponent(jPanel2)
													.addPreferredGap(
															javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
													.addGroup(
															jPanel1Layout
																	.createParallelGroup(
																			javax.swing.GroupLayout.Alignment.BASELINE)
																	.addComponent(jPanel3)
																	.addComponent(jPanel5))
													.addPreferredGap(
															javax.swing.LayoutStyle.ComponentPlacement.RELATED,
															10, Short.MAX_VALUE)
													.addComponent(jPanel4)
													.addGap(0, 0, 0)
													.addContainerGap()));

					main_status.setBorder(javax.swing.BorderFactory.createEtchedBorder());

					javax.swing.GroupLayout main_statusLayout = new javax.swing.GroupLayout(
							main_status);
					main_status.setLayout(main_statusLayout);
					main_statusLayout
							.setHorizontalGroup(main_statusLayout
									.createParallelGroup(
											javax.swing.GroupLayout.Alignment.LEADING)
									.addGroup(
											javax.swing.GroupLayout.Alignment.TRAILING,
											main_statusLayout
													.createSequentialGroup()
													.addComponent(
															main_time,
															javax.swing.GroupLayout.PREFERRED_SIZE,
															140,
															javax.swing.GroupLayout.PREFERRED_SIZE)
													.addComponent(
															start_time,
															javax.swing.GroupLayout.PREFERRED_SIZE,
															70,
															javax.swing.GroupLayout.PREFERRED_SIZE)
													.addComponent(
															nstart_time,
															javax.swing.GroupLayout.PREFERRED_SIZE,
															140,
															javax.swing.GroupLayout.PREFERRED_SIZE)
													.addComponent(
															end_time,
															javax.swing.GroupLayout.PREFERRED_SIZE,
															70,
															javax.swing.GroupLayout.PREFERRED_SIZE)
													.addComponent(
															nend_time,
															javax.swing.GroupLayout.PREFERRED_SIZE,
															140,
															javax.swing.GroupLayout.PREFERRED_SIZE)
													.addPreferredGap(
															javax.swing.LayoutStyle.ComponentPlacement.RELATED,
															10, Short.MAX_VALUE)
													.addComponent(
															status,
															javax.swing.GroupLayout.PREFERRED_SIZE,
															60,
															javax.swing.GroupLayout.PREFERRED_SIZE)));
					main_statusLayout
							.setVerticalGroup(main_statusLayout
									.createParallelGroup(
											javax.swing.GroupLayout.Alignment.LEADING)
									.addGroup(
											main_statusLayout
													.createSequentialGroup()
													.addGroup(
															main_statusLayout
																	.createParallelGroup(
																			javax.swing.GroupLayout.Alignment.LEADING)
																	.addComponent(
																			status,
																			javax.swing.GroupLayout.DEFAULT_SIZE,
																			17,
																			Short.MAX_VALUE)
																	.addComponent(
																			nend_time,
																			javax.swing.GroupLayout.DEFAULT_SIZE,
																			17,
																			Short.MAX_VALUE)
																	.addComponent(
																			end_time,
																			javax.swing.GroupLayout.DEFAULT_SIZE,
																			17,
																			Short.MAX_VALUE)
																	.addComponent(
																			nstart_time,
																			javax.swing.GroupLayout.DEFAULT_SIZE,
																			17,
																			Short.MAX_VALUE)
																	.addComponent(
																			start_time,
																			javax.swing.GroupLayout.DEFAULT_SIZE,
																			17,
																			Short.MAX_VALUE)
																	.addComponent(
																			main_time,
																			javax.swing.GroupLayout.DEFAULT_SIZE,
																			javax.swing.GroupLayout.DEFAULT_SIZE,
																			Short.MAX_VALUE))
													.addContainerGap()));
					
					lei.addActionListener(new java.awt.event.ActionListener(){
						@Override
						public void actionPerformed(ActionEvent e) {
							// TODO Auto-generated method stub
							lei_change(e);
						}
					});
					
					suanfa.addActionListener(new java.awt.event.ActionListener(){
						@Override
						public void actionPerformed(ActionEvent e) {
							// TODO Auto-generated method stub
							suanfa_change(e);
						}
					});
					
					trainbutton.addActionListener(new java.awt.event.ActionListener(){

						@Override
						public void actionPerformed(ActionEvent e) {
							// TODO Auto-generated method stub
							if("参数设置".equals(trainbutton.getText().trim()))
								trainbutton.setText("训练数据");
							else if("训练数据".equals(trainbutton.getText().trim()))
								trainbutton.setText("参数设置");
							train(e);
						}
                     });
					
					testbutton.addActionListener(new java.awt.event.ActionListener(){

						@Override
						public void actionPerformed(ActionEvent e) {
							// TODO Auto-generated method stub
							if("参数设置".equals(testbutton.getText().trim())&&!Utildata.isset){							
								testbutton.setText("测试数据");
								prebutton.setText("参数设置");
							}
							else if("测试数据".equals(testbutton.getText().trim())&&Utildata.isset){
								testbutton.setText("参数设置");
								prebutton.setText("参数设置");
							}
							try {
								test(e);
							} catch (IOException e1) {
								// TODO Auto-generated catch block
								e1.printStackTrace();
							}
						}
                     });
					
					prebutton.addActionListener(new java.awt.event.ActionListener(){

						@Override
						public void actionPerformed(ActionEvent e) {
							// TODO Auto-generated method stub
							if("参数设置".equals(prebutton.getText().trim())&&!Utildata.isset)
								prebutton.setText("预测数据");
							else if("预测数据".equals(prebutton.getText().trim())&&Utildata.isset)
								prebutton.setText("参数设置");
							try {
								pre(e);
							} catch (IOException e1) {
								// TODO Auto-generated catch block
								e1.printStackTrace();
							}
						}
                     });

					jMenu8.setText("绘图");
					jMenu8.setFont(new java.awt.Font("微软雅黑", 0, 14));

					drew_point.setFont(new java.awt.Font("微软雅黑", 0, 14));
					drew_point.setText("散点图");
					point_polar.setFont(new java.awt.Font("微软雅黑", 0, 14));
					point_polar.setText("极坐标");
					point_polar.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							point_polarActionPerformed(evt);
						}
					});
					drew_point.add(point_polar);
					point_3D.setFont(new java.awt.Font("微软雅黑", 0, 14));
					point_3D.setText("3D");
					point_3D.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							point_3DActionPerformed(evt);
						}
					});
					drew_point.add(point_3D);
					point_legend.setFont(new java.awt.Font("微软雅黑", 0, 14));
					point_legend.setText("有坐标线");
					point_legend.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							point_legendActionPerformed(evt);
						}
					});
					drew_point.add(point_legend);
					point_demo.setFont(new java.awt.Font("微软雅黑", 0, 14));
					point_demo.setText("无坐标线");
					point_demo.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							point_demoActionPerformed(evt);
						}
					});
					drew_point.add(point_demo);
					point_hist.setFont(new java.awt.Font("微软雅黑", 0, 14));
					point_hist.setText("统计量");
					point_hist.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							point_histActionPerformed(evt);
						}
					});
					drew_point.add(point_hist);
					jMenu8.add(drew_point);

					drew_line.setFont(new java.awt.Font("微软雅黑", 0, 14));
					drew_line.setText("折线图");
					line_demo.setFont(new java.awt.Font("微软雅黑", 0, 14));
					line_demo.setText("无坐标线");
					line_demo.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							line_demoActionPerformed(evt);
						}
					});
					drew_line.add(line_demo);
					line_dash.setFont(new java.awt.Font("微软雅黑", 0, 14));
					line_dash.setText("修改样式");
					line_dash.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							line_dashActionPerformed(evt);
						}
					});
					drew_line.add(line_dash);
					line_3D.setFont(new java.awt.Font("微软雅黑", 0, 14));
					line_3D.setText("3D");
					line_3D.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							line_3DActionPerformed(evt);
						}
					});
					drew_line.add(line_3D);
					
					jMenu8.add(drew_line);
					
					drew_lifang.setFont(new java.awt.Font("微软雅黑", 0, 14));
					drew_lifang.setText("直方图");
					bar_demo.setFont(new java.awt.Font("微软雅黑", 0, 14));
					bar_demo.setText("纵向");
					bar_demo.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							bar_demoActionPerformed(evt);
						}
					});
					drew_lifang.add(bar_demo);
					bar_barh.setFont(new java.awt.Font("微软雅黑", 0, 14));
					bar_barh.setText("横向");
					bar_barh.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							bar_barhActionPerformed(evt);
						}
					});
					drew_lifang.add(bar_barh);
					bar_polar.setFont(new java.awt.Font("微软雅黑", 0, 14));
					bar_polar.setText("极坐标");
					bar_polar.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							bar_polarActionPerformed(evt);
						}
					});
					drew_lifang.add(bar_polar);
					jMenu8.add(drew_lifang);
					
					drew_crcle.setFont(new java.awt.Font("微软雅黑", 0, 14));
					drew_crcle.setText("饼形图");
					pie_demo.setFont(new java.awt.Font("微软雅黑", 0, 14));
					pie_demo.setText("饼形图");
					pie_demo.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							pie_demoActionPerformed(evt);
						}
					});
					drew_crcle.add(pie_demo);
					
					jMenu8.add(drew_crcle);
					
					jMenuBar1.add(jMenu8);
					
					jMenu3.setText("数据库");
					jMenu3.setFont(new java.awt.Font("微软雅黑", 0, 14));

					jMenu10.setText("查询 ");
					jMenu10.setFont(new java.awt.Font("微软雅黑", 0, 14));

					jMenuItem21.setFont(new java.awt.Font("微软雅黑", 0, 14));
					jMenuItem21.setText("所有表  ");
					jMenuItem21.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							jMenuItem21ActionPerformed(evt);
						}
					});
					jMenu10.add(jMenuItem21);
					
					jMenuItem11.setFont(new java.awt.Font("微软雅黑", 0, 14));
					jMenuItem11.setText("指定表  ");
					jMenuItem11.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							jMenuItem21ActionPerformed(evt);
						}
					});
					jMenu10.add(jMenuItem11);

					jMenu3.add(jMenu10);

					jMenuItem23.setFont(new java.awt.Font("微软雅黑", 0, 14));
					jMenuItem23.setText("存储");
					jMenuItem23.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							jMenuItem23ActionPerformed(evt);
						}
					});
					
					jMenu3.add(jMenuItem23);
					jMenuBar1.add(jMenu3);


					jMenu4.setText("\u5e2e\u52a9");
					jMenu4.setFont(new java.awt.Font("微软雅黑", 0, 14));

					jMenuItem17.setFont(new java.awt.Font("微软雅黑", 0, 14));
					jMenuItem17.setText("About");
					jMenuItem17.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							jMenuItem17ActionPerformed(evt);
						}
					});
					jMenu4.add(jMenuItem17);

					jMenuItem18.setFont(new java.awt.Font("微软雅黑", 0, 14));
					jMenuItem18.setText("help");
					jMenuItem18.addActionListener(new java.awt.event.ActionListener() {
						public void actionPerformed(java.awt.event.ActionEvent evt) {
							jMenuItem18ActionPerformed(evt);
						}
					});
					jMenu4.add(jMenuItem18);

					jMenuBar1.add(jMenu4);

					setJMenuBar(jMenuBar1);

					javax.swing.GroupLayout layout = new javax.swing.GroupLayout(
							getContentPane());
					getContentPane().setLayout(layout);
					layout.setHorizontalGroup(layout
							.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
							.addComponent(main_status,
									javax.swing.GroupLayout.DEFAULT_SIZE,
									javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
							.addComponent(jPanel1, javax.swing.GroupLayout.DEFAULT_SIZE,
									javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE));
					layout.setVerticalGroup(layout
							.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
							.addGroup(
									javax.swing.GroupLayout.Alignment.TRAILING,
									layout.createSequentialGroup()
											.addComponent(jPanel1,
													javax.swing.GroupLayout.PREFERRED_SIZE,
													javax.swing.GroupLayout.DEFAULT_SIZE,
													javax.swing.GroupLayout.PREFERRED_SIZE)
											.addPreferredGap(
													javax.swing.LayoutStyle.ComponentPlacement.RELATED,
													13, Short.MAX_VALUE)
											.addComponent(main_status,
													javax.swing.GroupLayout.PREFERRED_SIZE,
													30,
													javax.swing.GroupLayout.PREFERRED_SIZE)));

					pack();


			        //设置窗口关闭方式
					setDefaultCloseOperation(javax.swing.WindowConstants.DO_NOTHING_ON_CLOSE);
					this.addWindowListener(new WindowAdapter(){
						   public void windowClosing(WindowEvent e) {
						    if(JOptionPane.showConfirmDialog(null, "你确定要退出吗？","提示",JOptionPane.YES_NO_OPTION,JOptionPane.QUESTION_MESSAGE)==JOptionPane.YES_OPTION){
						     System.exit(0);}
						   }
					});
					
					//设置窗口风格
					try {
						UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
					} catch (ClassNotFoundException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					} catch (InstantiationException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					} catch (IllegalAccessException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					} catch (UnsupportedLookAndFeelException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					
				    new Thread() {
				        public void run() {
				        while (true) {
				        try {
				        /*comp.setValue(value++);
				        if (value == comp.getMaximum()) {
				        	value = 0;
				        //dialog.setVisible(false);
				        }*/
				        	if(value <= 20){
				        		runtext.append("》");
				        		value++;
				        	}
				        	else{
				        		runtext.setText("");
				        		value = 0;
				        	}
				        sleep(100);
				        } catch (Exception e) {

				        }
				        }
				        }
				        }.start();
					
					//添加时钟
					new Thread(){
						public void run(){
							while(true){
								main_time.setText(DateUtil.getDateTime());
								try {
									Thread.sleep(1000);
								} catch (InterruptedException e) {
									// TODO Auto-generated catch block
									e.printStackTrace();
								}
							}
						}
					}.start();
					/*new Thread(){
						public void run(){
							while(true){
								nstart_time.setText(DateUtil.getTime());
								try {
									Thread.sleep(1000);
								} catch (InterruptedException e) {
									// TODO Auto-generated catch block
									e.printStackTrace();
								}
							}
						}
					}.start();
					new Thread(){
						public void run(){
							while(true){
								nend_time.setText(DateUtil.getTime());
								try {
									Thread.sleep(1000);
								} catch (InterruptedException e) {
									// TODO Auto-generated catch block
									e.printStackTrace();
								}
							}
						}
					}.start();*/

					//设置Main的进度条
					status.setIndeterminate(true);
					
					//HEAD END
					
				}// </editor-fold>
				//GEN-END:initComponents

				private void jMenuItem18ActionPerformed(java.awt.event.ActionEvent evt) {
					//help
					try {
						Runtime.getRuntime().exec("cmd /c start help.chm");
					} catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
				
				@SuppressWarnings({ "unchecked" })
				private void lei_change(java.awt.event.ActionEvent evt){
					suanfa.removeAllItems();
					for(int i = 0;i<Utildata.label[lei.getSelectedIndex()].length;i++){
					suanfa.addItem(Utildata.label[lei.getSelectedIndex()][i]);
					}
				}
				
				private void suanfa_change(java.awt.event.ActionEvent evt){
					if(lei.getSelectedIndex()==0&&Utildata.list0_1.contains(suanfa.getSelectedIndex())||
			        		lei.getSelectedIndex()==1&&Utildata.list1_1.contains(suanfa.getSelectedIndex())||
			        		lei.getSelectedIndex()==2&&Utildata.list2_1.contains(suanfa.getSelectedIndex())||
			        		lei.getSelectedIndex()==3&&Utildata.list3_1.contains(suanfa.getSelectedIndex())||
			        		lei.getSelectedIndex()==4&&Utildata.list4_1.contains(suanfa.getSelectedIndex())||
			        		lei.getSelectedIndex()==5&&Utildata.list5_1.contains(suanfa.getSelectedIndex())){
						prebutton.setText("参数设置");
						jPanel5.removeAll();
						javax.swing.GroupLayout jPanel5Layout = new javax.swing.GroupLayout(jPanel5);
						jPanel5.setLayout(jPanel5Layout);
			        	jPanel5Layout
				        .setHorizontalGroup(jPanel5Layout
						.createParallelGroup(
								javax.swing.GroupLayout.Alignment.LEADING)
						.addGroup(
								javax.swing.GroupLayout.Alignment.TRAILING,
								jPanel5Layout
										.createSequentialGroup()
										.addContainerGap(100, Short.MAX_VALUE)
										.addComponent(
												prebutton,
												javax.swing.GroupLayout.PREFERRED_SIZE,
												100,
												javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(100, Short.MAX_VALUE)
										));
				
				jPanel5Layout
				.setVerticalGroup(jPanel5Layout
						.createParallelGroup(
								javax.swing.GroupLayout.Alignment.LEADING)
						.addGroup(
												jPanel5Layout
														.createParallelGroup(
																javax.swing.GroupLayout.Alignment.CENTER)
														.addComponent(
																prebutton,
																javax.swing.GroupLayout.DEFAULT_SIZE,
																17,
																Short.MAX_VALUE)
														.addGap(0,0,0)));
			        }
			        else if(lei.getSelectedIndex()==0&&Utildata.list0_2.contains(suanfa.getSelectedIndex())||
			        		lei.getSelectedIndex()==2&&Utildata.list2_2.contains(suanfa.getSelectedIndex())||
			        		lei.getSelectedIndex()==3&&Utildata.list3_2.contains(suanfa.getSelectedIndex())){
			        	testbutton.setText("参数设置");
			        	prebutton.setText("预测数据");
			        	jPanel5.removeAll();
			        	javax.swing.GroupLayout jPanel5Layout = new javax.swing.GroupLayout(jPanel5);
						jPanel5.setLayout(jPanel5Layout);
			        	jPanel5Layout
				        .setHorizontalGroup(jPanel5Layout
						.createParallelGroup(
								javax.swing.GroupLayout.Alignment.LEADING)
						.addGroup(
								javax.swing.GroupLayout.Alignment.TRAILING,
								jPanel5Layout
										.createSequentialGroup()
										.addContainerGap(10, Short.MAX_VALUE)
										.addComponent(
												testbutton,
												javax.swing.GroupLayout.PREFERRED_SIZE,
												100,
												javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(10, Short.MAX_VALUE)
										.addPreferredGap(
												javax.swing.LayoutStyle.ComponentPlacement.UNRELATED)
										.addComponent(prebutton,
												      javax.swing.GroupLayout.PREFERRED_SIZE, 
												      100,
												      javax.swing.GroupLayout.PREFERRED_SIZE)
										.addContainerGap(10, Short.MAX_VALUE)
										));
				
				jPanel5Layout
				.setVerticalGroup(jPanel5Layout
						.createParallelGroup(
								javax.swing.GroupLayout.Alignment.LEADING)
						.addGroup(
										jPanel5Layout
												.createParallelGroup(
														javax.swing.GroupLayout.Alignment.LEADING)
												.addComponent(
														testbutton,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														17,
														Short.MAX_VALUE)
												.addComponent(
														prebutton,
														javax.swing.GroupLayout.DEFAULT_SIZE,
														17,
														Short.MAX_VALUE)));
			        }
					jPanel5.updateUI();
				}
				
				private void train(java.awt.event.ActionEvent evt){
					
				}
				
				private void test(java.awt.event.ActionEvent evt) throws IOException{
					if(!Utildata.isset){
					if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==5||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==0){
						KNN temp = new KNN();
						jPanel4.removeAll();
						jPanel4.add(temp.jpanel1);
					}
					else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==6||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==1){

						Tree temp = new Tree();
						jPanel4.removeAll();
						jPanel4.add(temp.jpanel1);
					}
					else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==9||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==4){

						Logistic_grad temp = new Logistic_grad();
						jPanel4.removeAll();
						jPanel4.add(temp.jpanel1);
					}
					else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==10||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==5){

						Logistic_stoc temp = new Logistic_stoc();
						jPanel4.removeAll();
						jPanel4.add(temp.jpanel1);
					}
					else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==11||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==6){

						Logistic_toc temp = new Logistic_toc();
						jPanel4.removeAll();
						jPanel4.add(temp.jpanel1);
					}
					else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==12||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==7){

						MLIA temp = new MLIA();
						jPanel4.removeAll();
						jPanel4.add(temp.jpanel1);
					}
					else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==13||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==8){

						SMO temp = new SMO();
						jPanel4.removeAll();
						jPanel4.add(temp.jpanel1);
					}
					else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==14||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==9){

						Adaboost temp = new Adaboost();
						jPanel4.removeAll();
						jPanel4.add(temp.jpanel1);
					}
					else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==19||lei.getSelectedIndex()==3&&suanfa.getSelectedIndex()==4){

						Regtree temp = new Regtree();
						jPanel4.removeAll();
						jPanel4.add(temp.jpanel1);
					}
					else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==20||lei.getSelectedIndex()==3&&suanfa.getSelectedIndex()==5){

						Modeltree temp = new Modeltree();
						jPanel4.removeAll();
						jPanel4.add(temp.jpanel1);
					}
					}
					else if(Utildata.isset){
						jPanel4.removeAll();
						jPanel4.add(rolltext);						
						Utildata.isset = false;
						run = true;
						nstart_time.setText(DateUtil.getTime());
						ProcessBuilder processBuilder = new ProcessBuilder();
						URL str = this.getClass().getClassLoader().getResource("com/machine/python");
						String[] indextest = Choosepython.choosetest(lei.getSelectedIndex(), suanfa.getSelectedIndex());
						System.out.println(indextest);
						processBuilder.command(indextest);  
						processBuilder.directory(new File(str.getPath()));//切换工作目录 
						processBuilder.redirectErrorStream(true);  
						java.lang.Process process = processBuilder.start();  
						StringBuilder result = new StringBuilder();  
						final BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));  
						try {  
						       String line;  
						       while ((line = reader.readLine()) != null) {  
						           result.append(line);  
						           text.append(line + "\n");
						       }  
						} catch (IOException e) {  
						       text.append("failed to read output from process");  
						} finally {  
						       reader.close();
						       run = false;
						       nend_time.setText(DateUtil.getTime());
						}
					}
				}
				
				private void pre(java.awt.event.ActionEvent evt) throws IOException{
					if(!Utildata.isset){
						if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==0||lei.getSelectedIndex()==1&&suanfa.getSelectedIndex()==0){
							Mean temp = new Mean();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==1||lei.getSelectedIndex()==1&&suanfa.getSelectedIndex()==1){

							Average temp = new Average();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==2||lei.getSelectedIndex()==1&&suanfa.getSelectedIndex()==2){

							Std temp = new Std();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==3||lei.getSelectedIndex()==1&&suanfa.getSelectedIndex()==3){

							Min temp = new Min();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==4||lei.getSelectedIndex()==1&&suanfa.getSelectedIndex()==4){

							Max temp = new Max();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==5||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==0){

							KNN temp = new KNN();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==6||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==1){

							Tree temp = new Tree();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==7||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==2){

							Bayes_two temp = new Bayes_two();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==8||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==3){

							Bayes_more temp = new Bayes_more();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==9||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==4){

							Logistic_grad temp = new Logistic_grad();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==10||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==5){

							Logistic_stoc temp = new Logistic_stoc();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==11||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==6){

							Logistic_toc temp = new Logistic_toc();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==12||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==7){

							MLIA temp = new MLIA();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==13||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==8){

							SMO temp = new SMO();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==14||lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==9){

							Adaboost temp = new Adaboost();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==15||lei.getSelectedIndex()==3&&suanfa.getSelectedIndex()==0){

							Stand temp = new Stand();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==16||lei.getSelectedIndex()==3&&suanfa.getSelectedIndex()==1){

							Lwlr temp = new Lwlr();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==17||lei.getSelectedIndex()==3&&suanfa.getSelectedIndex()==2){

							Ridge temp = new Ridge();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==18||lei.getSelectedIndex()==3&&suanfa.getSelectedIndex()==3){

							Stage temp = new Stage();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==19||lei.getSelectedIndex()==3&&suanfa.getSelectedIndex()==4){

							Regtree temp = new Regtree();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==20||lei.getSelectedIndex()==3&&suanfa.getSelectedIndex()==5){

							Modeltree temp = new Modeltree();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==21||lei.getSelectedIndex()==4&&suanfa.getSelectedIndex()==0){

							Kmeans temp = new Kmeans();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==22||lei.getSelectedIndex()==4&&suanfa.getSelectedIndex()==0){

							Apriori temp = new Apriori();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						else if(lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==23||lei.getSelectedIndex()==4&&suanfa.getSelectedIndex()==1){

							FP temp = new FP();
							jPanel4.removeAll();
							jPanel4.add(temp.jpanel2);
						}
						}
						else if(Utildata.isset){
							jPanel4.removeAll();
							jPanel4.add(rolltext);
							Utildata.isset = false;
							run = true;
							nstart_time.setText(DateUtil.getTime());
							if((lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==7)||
							    (lei.getSelectedIndex()==0&&suanfa.getSelectedIndex()==8)||
							    (lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==2)||
							    (lei.getSelectedIndex()==2&&suanfa.getSelectedIndex()==3)){
								
							}
							else{
							File file = new File(Pythondata.outfile);
							if(file.isDirectory()){
							     File newfile = new File(Pythondata.outfile +"/"+"output");
							     if(newfile.exists()){
							    	 newfile.delete();
							     }
							     newfile.createNewFile();
							     Pythondata.outfile = Pythondata.outfile + "/" + "output";
							}
							}
							ProcessBuilder processBuilder = new ProcessBuilder();
							URL str = this.getClass().getClassLoader().getResource("com/machine/python");
							String[] indexpre = Choosepython.choosepre(lei.getSelectedIndex(), suanfa.getSelectedIndex());
							processBuilder.command(indexpre);  
							processBuilder.directory(new File(str.getPath()));//切换工作目录 
							processBuilder.redirectErrorStream(true);  
							java.lang.Process process = processBuilder.start();  
							StringBuilder result = new StringBuilder();  
							final BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));  
							try {  
							       String line;  
								   text.setText("");
							       while ((line = reader.readLine()) != null) {  
							           result.append(line);  
							           text.append(line + "\n");
							       }  
							} catch (IOException e) {  
							       text.append("failed to read output from process");  
							} finally {  
							       reader.close();
							       run = false;
							       nend_time.setText(DateUtil.getTime());
							}
						}
				}

				private void jMenuItem17ActionPerformed(java.awt.event.ActionEvent evt) {
					//帮助
					
				}

				private void jMenuItem23ActionPerformed(java.awt.event.ActionEvent evt) {
					//读者查询-by 编号
					
				}

				private void jMenuItem21ActionPerformed(java.awt.event.ActionEvent evt) {
					//图书查询-by 编号
					
				}

				private void point_polarActionPerformed(java.awt.event.ActionEvent evt){
					Point_polar temp = new Point_polar();
					jPanel4.removeAll();
					jPanel4.add(temp.jpanel2);
				}
				private void point_3DActionPerformed(java.awt.event.ActionEvent evt){
					Point_3D temp = new Point_3D();
					jPanel4.removeAll();
					jPanel4.add(temp.jpanel2);
				}
				private void point_legendActionPerformed(java.awt.event.ActionEvent evt){
					Point_legend temp = new Point_legend();
					jPanel4.removeAll();
					jPanel4.add(temp.jpanel2);
				}
				private void point_histActionPerformed(java.awt.event.ActionEvent evt){
					Point_hist temp = new Point_hist();
					jPanel4.removeAll();
					jPanel4.add(temp.jpanel2);
				}
				private void point_demoActionPerformed(java.awt.event.ActionEvent evt){
					Point_demo temp = new Point_demo();
					jPanel4.removeAll();
					jPanel4.add(temp.jpanel2);
				}
				private void pie_demoActionPerformed(java.awt.event.ActionEvent evt){
					Pie_demo temp = new Pie_demo();
					jPanel4.removeAll();
					jPanel4.add(temp.jpanel2);
				}
				private void line_dashActionPerformed(java.awt.event.ActionEvent evt){
					Line_demo temp = new Line_demo();
					jPanel4.removeAll();
					jPanel4.add(temp.jpanel2);
				}
				private void line_demoActionPerformed(java.awt.event.ActionEvent evt){
					Line_dash temp = new Line_dash();
					jPanel4.removeAll();
					jPanel4.add(temp.jpanel2);
				}
				private void line_3DActionPerformed(java.awt.event.ActionEvent evt){
					Line_3D temp = new Line_3D();
					jPanel4.removeAll();
					jPanel4.add(temp.jpanel2);
				}
				private void bar_demoActionPerformed(java.awt.event.ActionEvent evt){
					Bar_demo temp = new Bar_demo();
					jPanel4.removeAll();
					jPanel4.add(temp.jpanel2);
				}
				private void bar_barhActionPerformed(java.awt.event.ActionEvent evt){
					Bar_barh temp = new Bar_barh();
					jPanel4.removeAll();
					jPanel4.add(temp.jpanel2);
				}
				private void bar_polarActionPerformed(java.awt.event.ActionEvent evt){
					Bar_polar temp = new Bar_polar();
					jPanel4.removeAll();
					jPanel4.add(temp.jpanel2);
				}
				/**
				 * @param args the command line arguments
				 */
				public static void start() {
					java.awt.EventQueue.invokeLater(new Runnable() {
						public void run() {
							new Main().setVisible(true);
						}
					});
				}

				//GEN-BEGIN:variables
				// Variables declaration - do not modify
				private javax.swing.JMenuItem drew_point;
				private javax.swing.JMenuItem drew_line;
				private javax.swing.JMenu jMenu10;
				private javax.swing.JMenu jMenu3;
				private javax.swing.JMenu jMenu4;
				private javax.swing.JMenu jMenu8;
				private javax.swing.JMenuBar jMenuBar1;
				private javax.swing.JMenuItem drew_lifang;
				private javax.swing.JMenuItem drew_crcle;
				private javax.swing.JMenuItem jMenuItem11;
				private javax.swing.JMenuItem jMenuItem17;
				private javax.swing.JMenuItem jMenuItem18;
				private javax.swing.JMenuItem jMenuItem21;
				private javax.swing.JMenuItem jMenuItem23;
				private javax.swing.JPanel jPanel1;
				private javax.swing.JPanel main_status;
				private javax.swing.JPanel jPanel2;
				private javax.swing.JPanel jPanel3;
				private javax.swing.JPanel jPanel4;	
				private javax.swing.JPanel jPanel5;
				private javax.swing.JLabel main_time;
				private javax.swing.JProgressBar status;
				private javax.swing.JLabel start_time;
				private javax.swing.JLabel end_time;
				private javax.swing.JLabel nstart_time;
				private javax.swing.JLabel nend_time;
				private JTextArea text;
				private JProgressBar comp;
				private JComboBox<Object> lei;
				private JComboBox<String> suanfa;
				private JButton train;
				private JButton test;
				private JScrollPane rolltext;
				private JButton trainbutton;
				private JButton testbutton;
				private JButton prebutton;
				private JTextArea runtext;
				private JMenuItem bar_demo;
				private JMenuItem bar_barh;
				private JMenuItem bar_polar;
				private JMenuItem pie_demo;
				private JMenuItem point_polar;
				private JMenuItem point_3D;
				private JMenuItem point_legend;
				private JMenuItem point_demo;
				private JMenuItem point_hist;
				private JMenuItem line_dash;
				private JMenuItem line_demo;
				private JMenuItem line_3D;
				// End of variables declaration//GEN-END:variables
				
				public static void main(String[] args){
					Main.start();
				}

			}
