db = db.getSiblingDB("test");
for(var i=1;i<=1000;i++) db.c1.save({id:i,value1:"你好"});
db.c1.stats();

//插入五百万数据
for(var i=0; i<5000000; i++){
    db.test1.insert({name : "mongodb_test" + i,seq : i});
}
db.test1.stats();

//插入一千万数据
for(var i=0; i<10000000; i++){
    db.test2.insert({name : "mongodb_test"+ i,seq : i});
}
db.test2.stats();
