module andgate(a, o, d);
	input[31:0] a;
	input[31:0] d;
	output reg o;
	always @(a) 
		#d o = &a;
endmodule
