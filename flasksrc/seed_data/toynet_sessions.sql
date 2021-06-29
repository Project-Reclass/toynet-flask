BEGIN TRANSACTION;

INSERT INTO toynet_topos (topo_id, topology, author_id) VALUES(1, '<?xml version="1.0" encoding="UTF-8"?><topology><root>r1</root><routerList><router name="r1" ip="172.16.0.1/24"><intf>10.0.0.1/30</intf><intf>172.16.0.1/24</intf><intf>172.16.1.1/24</intf></router></routerList><switchList><switch name="s1" /><switch name="s2" /></switchList><hostList><host name="h1" ip="172.16.0.2/24"><defaultRouter><name>r1</name><intf>1</intf></defaultRouter></host><host name="h2" ip="172.16.1.2/24"><defaultRouter><name>r1</name><intf>2</intf></defaultRouter></host></hostList><linkList><link><dvc name="r1"><intf>1</intf></dvc><dvc name="s1"><intf>0</intf></dvc></link><link><dvc name="r1"><intf>2</intf></dvc><dvc name="s2"><intf>0</intf></dvc></link><link><dvc name="s1"><intf>1</intf></dvc><dvc name="h1" /></link><link><dvc name="s2"><intf>1</intf></dvc><dvc name="h2" /></link></linkList></topology>', 0);

INSERT INTO toynet_sessions (session_id, topo_id, topology, user_id, create_time, update_time) VALUES(1,1, '<?xml version="1.0" encoding="UTF-8"?><topology><root>r1</root><routerList><router name="r1" ip="172.16.0.1/24"><intf>10.0.0.1/30</intf><intf>172.16.0.1/24</intf><intf>172.16.1.1/24</intf></router></routerList><switchList><switch name="s1" /><switch name="s2" /></switchList><hostList><host name="h1" ip="172.16.0.2/24"><defaultRouter><name>r1</name><intf>1</intf></defaultRouter></host><host name="h2" ip="172.16.1.2/24"><defaultRouter><name>r1</name><intf>2</intf></defaultRouter></host></hostList><linkList><link><dvc name="r1"><intf>1</intf></dvc><dvc name="s1"><intf>0</intf></dvc></link><link><dvc name="r1"><intf>2</intf></dvc><dvc name="s2"><intf>0</intf></dvc></link><link><dvc name="s1"><intf>1</intf></dvc><dvc name="h1" /></link><link><dvc name="s2"><intf>1</intf></dvc><dvc name="h2" /></link></linkList></topology>', '0', "2020-08-14T23:15:54.840055Z", "2020-08-14T23:15:54.840097Z");

END TRANSACTION;
