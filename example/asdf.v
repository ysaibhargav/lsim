module circuit();

	reg i0, i1, i2, i3;
	wire w21, w02, w12;
	output o0;
	assign {w21} = {o0};
	
	andgate and0(.a(32'b11111111111111111111111111111100+{i0, i1}), .o(w02), .d(0));
	andgate and1(.a(32'b11111111111111111111111111111000+{w21, i2, i3}), .o(w12), .d(0));
	orgate or0(.a(32'b0+{w02, w12}), .o(o0), .d(0));
	
	initial begin
		$dumpfile("test.vcd");
		$dumpvars(0, circuit);
		/*Write code for inputs here
		*
		*
		*
		*
		*
		*
		*
		*
		*/
	end

endmodule