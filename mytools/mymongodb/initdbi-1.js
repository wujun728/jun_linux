printjson(1);
config={_id: 'rs1', members:[{_id: 0,host:'172.17.0.94:27017'},{_id:1,host:'172.17.0.91:27017'},{_id:2,host:'172.17.0.92:27017'}]}
rs.initiate(config);
