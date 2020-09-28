#!/usr/bin/env python

import sys
import os.path
from os.path import join as PJ
import re
import json
import numpy as np
from tqdm import tqdm
import igraph as ig
import jgf
import pandas as pd

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numbers

def isFloat(value):
	if(value is None):
		return False
	try:
		numericValue = float(value)
		return np.isfinite(numericValue)
	except ValueError:
		return False


def isNumberObject(value):
	return isinstance(value, numbers.Number)

class NumpyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
			np.int16, np.int32, np.int64, np.uint8,
			np.uint16, np.uint32, np.uint64)):
			ret = int(obj)
		elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
			ret = float(obj)
		elif isinstance(obj, (np.ndarray,)): 
			ret = obj.tolist()
		else:
			ret = json.JSONEncoder.default(self, obj)

		if isinstance(ret, (float)):
			if math.isnan(ret):
				ret = None

		if isinstance(ret, (bytes, bytearray)):
			ret = ret.decode("utf-8")

		return ret

results = {"errors": [], "warnings": [], "brainlife": [], "datatype_tags": [], "tags": []}

def warning(msg):
	global results
	results['warnings'].append(msg) 
	#results['brainlife'].append({"type": "warning", "msg": msg}) 
	print(msg)

def error(msg):
	global results
	results['errors'].append(msg) 
	#results['brainlife'].append({"type": "error", "msg": msg}) 
	print(msg)

def exitApp():
	global results
	with open("product.json", "w") as fp:
		json.dump(results, fp, cls=NumpyEncoder)
	if len(results["errors"]) > 0:
		sys.exit(1)
	else:
		sys.exit()

def exitAppWithError(msg):
	global results
	results['errors'].append(msg) 
	#results['brainlife'].append({"type": "error", "msg": msg}) 
	print(msg)
	exitApp()


configFilename = "config.json"
argCount = len(sys.argv)
if(argCount > 1):
		configFilename = sys.argv[1]

outputDirectory = "output"
figuresOutputDirectory = PJ(outputDirectory,"figures")

with open("template/index.html", "r") as fd:
	htmlTemplate = fd.read();

with open("template/styles.css", "r") as fd:
	stylesTemplate = fd.read();

if(not os.path.exists(outputDirectory)):
		os.makedirs(outputDirectory)

if(not os.path.exists(figuresOutputDirectory)):
		os.makedirs(figuresOutputDirectory)

with open(configFilename, "r") as fd:
		config = json.load(fd)

# "transform":"absolute", //"absolute" or "signed"
# "retain-weights":false,
# "threshold": "none"

networks = jgf.igraph.load(config["network"], compressed=True)

nullNetworks = None
if("nullmodels" in config and config["nullmodels"]):
	nullNetworks = jgf.igraph.load(config["nullmodels"], compressed=True)

binsCount = 25

if(len(networks)>1):
	warning("Input files have more than one network. Only the first entry was used to compose the report.")
	
if(len(networks)==0):
	exitAppWithError("The network file should contain at least one network.")
else:
	network = networks[0];

	networkAttributesKeys = network.attributes()
	networkAttributes = [[] for _ in networkAttributesKeys];

	distributionPlots = [];
	for keyIndex,key in enumerate(networkAttributesKeys):
		value = network[key]
		if(isFloat(value)):
			networkAttributes[keyIndex].append("%.3g"%value)
		else:
			networkAttributes[keyIndex].append(value)
		if(nullNetworks):
			nullValues = []
			if(isFloat(value)):
				for nullNetwork in nullNetworks:
					if(key in nullNetwork.attributes()):
						if(isFloat(nullNetwork[key])):
							nullValues.append(nullNetwork[key]);
			if(nullValues):
				nullAverage = np.average(nullValues)
				nullStd = np.std(nullValues)
				networkAttributes[keyIndex].append("%.3g ± %.3g"%(nullAverage,nullStd))
				if(isFloat(value) and nullStd>0):
					_,bins = np.histogram([value]+nullValues)
					fig = plt.figure(figsize= (6,3.0))
					ax = plt.axes()
					ax.hist(nullValues,bins=bins,density=True,color="#888888")
					# ax.hist([value],bins=bins,density=True,color="#cc1111")
					trans = ax.get_xaxis_transform()
					ax.axvline(x=value,linewidth=3.0,color="#cc1111")
					plt.text(value, 0.99, 'network',color="#770000",horizontalalignment="right",verticalalignment="top", transform=trans,rotation=90)
					ax.set_xlabel(key);
					ax.set_ylabel("Density");
					plt.tight_layout()
					fig.savefig(PJ(figuresOutputDirectory,"network_hist_%s.png"%(key)),dpi=200);
					fig.savefig(PJ(figuresOutputDirectory,"network_hist_%s.pdf"%(key)));
					plt.close(fig)
					distributionPlots.append(key)
			else:
				networkAttributes[keyIndex].append("-")
	
	
	vertexAttributesKeys = network.vertex_attributes()

	vertexDistributionPlots = [];
	for keyIndex,key in enumerate(vertexAttributesKeys):
		
		values = network.vs[key]

		if(np.all([isNumberObject(value) for value in values])):
			dataToCalculateBins = []+values;
			nullValues = []
			if(nullNetworks):
				for nullNetwork in nullNetworks:
					if(key in nullNetwork.vertex_attributes()):
						if(np.all([isNumberObject(value) for value in nullNetwork.vs[key]])):
							nullValues.append(nullNetwork.vs[key]);
							dataToCalculateBins+=nullNetwork.vs[key];
				
			allData = np.array(dataToCalculateBins)
			minAllData = np.min(allData)
			maxAllData = np.max(allData)
			bins = None;
			useLog = False;
			if(minAllData>=0 and np.sum(allData>0)>=0.5*len(allData)): #Less than 50% zeros
				minNonZero = np.min(allData[allData>0]);
				if(maxAllData/minNonZero>100):
					bins = np.logspace(np.log10(minNonZero),np.log10(maxAllData),binsCount);
					useLog=True;
					
			if(bins is None):
				_,bins = np.histogram(allData)

			if(nullValues):
				nullDistribs = []
				for nullValuesEntry in nullValues:
					distrib,bins = np.histogram(nullValuesEntry,bins=bins,density=True)
					nullDistribs.append(distrib)
				nullAverages = np.average(nullDistribs,axis=0)
				nullStds = np.std(nullDistribs,axis=0)
					
			fig = plt.figure(figsize= (6,3.0))
			ax = plt.axes()
			xbins = (bins[:-1]+bins[1:])*0.5
			ax.hist(values,bins=bins,density=True,color="#cc1111",label="Network")
			if(nullValues):
				ax.fill_between(xbins,np.clip(nullAverages-nullStds,0,None),nullAverages+nullStds,color="#888888",alpha=0.25,zorder=10)
				ax.plot(xbins,nullAverages,color="#888888",label="Null model")
				ax.legend()
			ax.set_xlabel(key);
			ax.set_ylabel("Density");
			if(useLog):
				ax.set_xscale("log")
				ax.set_yscale("log")
			plt.tight_layout()
			fig.savefig(PJ(figuresOutputDirectory,"nodes_hist_%s.png"%(key)),dpi=200);
			fig.savefig(PJ(figuresOutputDirectory,"nodes_hist_%s.pdf"%(key)));
			plt.close(fig)
			vertexDistributionPlots.append(key)


	columns = ["Value"]
	if(nullNetworks):
		columns+=["Null-model (avg ± std)"]
	
	df = pd.DataFrame(np.array(networkAttributes),columns = columns,index=networkAttributesKeys);
	tableHTML = df.to_html(border=0,classes="pure-table pure-table-striped",justify="center") \
		.replace("<td>","<td style=\"text-align: center;\">") \
		.replace("<tr>","<tr style=\"text-align: right;\">");
	htmlTemplate = htmlTemplate.replace("%%MEASUREMENTS_TABLE%%",tableHTML)
	
	if(distributionPlots):
		htmlTemplate = htmlTemplate.replace("%%HAS_DISTRIBUTIONS%%","")
		imagesHTML = ""
		for key in distributionPlots:
			imagesHTML += "<a href=\"%s\"><img class=\"pure-img\" src=\"%s\" onload=\"this.width/=2;\" ></a>"%("figures/network_hist_%s.pdf"%(key),"figures/network_hist_%s.png"%(key))
		htmlTemplate = htmlTemplate.replace("%%DISTRIBUTIONS%%",imagesHTML)
	else:
		htmlTemplate = htmlTemplate.replace("%%HAS_DISTRIBUTIONS%%","style=\"display:none\"")
	
	if(vertexDistributionPlots):
		htmlTemplate = htmlTemplate.replace("%%HAS_NODEDISTRIBUTIONS%%","")
		imagesHTML = ""
		for key in vertexDistributionPlots:
			imagesHTML += "<a href=\"%s\"><img class=\"pure-img\" src=\"%s\" onload=\"this.width/=2;\" ></a>"%("figures/nodes_hist_%s.pdf"%(key),"figures/nodes_hist_%s.png"%(key))
		htmlTemplate = htmlTemplate.replace("%%NODEDISTRIBUTIONS%%",imagesHTML)
	else:
		htmlTemplate = htmlTemplate.replace("%%HAS_NODEDISTRIBUTIONS%%","style=\"display:none\"")
	

with open(PJ(outputDirectory,"index.html"), "w") as fd:
	fd.write(htmlTemplate);

with open(PJ(outputDirectory,"styles.css"), "w") as fd:
	fd.write(stylesTemplate);

exitApp()