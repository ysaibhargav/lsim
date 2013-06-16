module orgate(a, o, d);
	input[31:0] a, d;
	output reg o;
	always @(a)
		#d o = |a;
endmodule
