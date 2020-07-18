URL := http://www.cikrf.ru/services/opendata/?id=100100084849066&id2=0&type=227

data.xml:
	curl -s '${URL}' > data.xml
