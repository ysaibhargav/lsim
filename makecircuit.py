import sys
from graph_tool.all import *

gin = sys.argv[2]
fout = sys.argv[1]

g = load_graph(gin)

f = open(fout, 'w')

header = "module circuit();\n"
footer = "endmodule"

"""Wire declaration"""
wd = "wire "
""""Input declaration"""
ind = "reg "
"""Module declaration"""
md = ""
"""Output declaration"""
od = "output "
"""Assign statements"""
asg = ""

"""Output count for identifier nomenclature"""
oc = 0
"""Input count for identifier nomenclature"""
inc = 0
"""Wire count"""
wc = 0
"""Andgate count"""
andc = 0
"""Orgate count"""
orc = 0
nandc = 0
norc = 0


n = g.num_vertices()
m = g.num_edges()
i = g.graph_properties['inputs']
o = g.graph_properties['outputs']

for v in g.vertices():
	name = g.vertex_properties["type"][v]
	if name == "and":
		md = md+name+"gate "+name+str(andc)+"("
		andc = andc + 1 
	elif name == "or":
		md = md+name+"gate "+name+str(orc)+"("
		orc = orc + 1
	elif name == "nand":
		md = md+name+"gate "+name+str(nandc)+"("
		nandc = nandc + 1
	elif name == "nor":
		md = md+name+"gate "+name+str(norc)+"("
		norc = norc + 1
	nin_ = g.vertex_properties["num_inputs"][v]
	nin = nin_
	andinput = ""
	inpcon = ""
	while nin_ > 0:
		"""Input declaration"""
		nin_ = nin_ - 1
		ind = ind + "i" + str(inc)
		inpcon = inpcon + "i" + str(inc) + ", "
		inc = inc + 1
		if inc == i:
			ind = ind + ";\n"
		else:
			ind = ind + ", "
	if name == "and" or name == "nand":
		andinput = ".a(32'b" + '1'*(32-nin-g.vertex(v).in_degree()) + '0'*(nin+g.vertex(v).in_degree()) + "+" + "{"
	elif name == "or" or name == "nor":
		andinput = ".a(32'b0" + "+" + "{"
	
	wc_ = 0

	for e in v.in_edges():
		edge = "w"+str(e.source())+str(e.target())
		wd = wd + edge
		wc = wc + 1
		wc_ = wc_ + 1
		if wc == m:
			wd = wd + ";\n"
		else:
			wd = wd + ", "
		andinput = andinput + edge
		if wc_ == v.in_degree() and nin == 0:
			andinput = andinput + "}), "
		else:
			andinput = andinput + ", "

	"""concetenation of inputs"""
	if inpcon != '':
		inpcon = inpcon[0:len(inpcon)-2]
		inpcon = inpcon + "}), "
		andinput = andinput + inpcon

	andinput = andinput + ".o("
	if g.vertex_properties['pos'][v] == 1:
		od = od + "o" + str(oc)
		andinput = andinput + "o" + str(oc)
		if v.out_degree() > 0:
			rhs = "{" + ("o" + str(oc) + ", ") * v.out_degree()
			rhs = rhs[0:len(rhs)-2] + "};"
			lhs = "{"
			for e in v.out_edges():
				lhs = lhs + "w" + str(e.source()) + str(e.target()) + ", "
			lhs = lhs[0:len(lhs)-2] + "}"
			asg = asg + "assign " + lhs + " = " + rhs + "\n\t"
		oc = oc + 1
		if oc == o:
			od = od + ";\n"
		else:
			od = od + ", "		
	else:
		for e in v.out_edges():
			wij = "w" + str(e.source())+str(e.target())
			andinput = andinput + wij 
			break
		if v.out_degree() > 1:
			temp = 0
			rhs = "{" + (wij + ", ") * (v.out_degree() - 1)
			rhs = rhs[0:len(rhs)-2] + "};"
			lhs = "{"
			for e in v.out_edges():
				if temp == 0:
					temp = 1
					continue
				lhs = lhs + "w" + str(e.source()) + str(e.target()) + ", "
			lhs = lhs[0:len(lhs)-2] + "}"
			asg = asg + "assign " + lhs + " = " + rhs + "\n\t"
				
	andinput = andinput + "), "
	md = md + andinput + ".d(" + str(g.vertex_properties['delay'][v]) + "));\n\t" 	

	body = "\tinitial begin\n"
	body = body + "\t\t$dumpfile(\"test.vcd\");\n\t\t$dumpvars(0, circuit);\n\t\t/*Write code for inputs here\n" + "\t\t*\n" * 8 + "\t\t*/\n"
	body = body + "\tend\n"

f.write(header+"\n\t"+ind+"\t"+wd+"\t"+od+"\t"+asg+"\n\t"+md+"\n"+body+"\n"+footer)
