#include <logisim.h>
#include <stdio.h>

// W, X, Y, Z represent the 4 bits of our counter (W is MSB, Z is LSB)
wire W, X, Y, Z, W1, X1, Y1, Z1, A, B, C, D, E, F, G;

// 4 registers for the 4-bit state machine (Counting 0-9 requires 4 bits)
reg b3 = {.in = &W1, .out = &W};
reg b2 = {.in = &X1, .out = &X};
reg b1 = {.in = &Y1, .out = &Y};
reg b0 = {.in = &Z1, .out = &Z};

int main() {
    CLOCK_CYCLE {
        // --- Helper signals for logic ---
        wire notW = NOT(W);
        wire notX = NOT(X);
        wire notY = NOT(Y);
        wire notZ = NOT(Z);
        wire yz   = AND(Y, Z);
        
        wire D_1 = AND(notX, notZ);
        wire D_2 = AND(notX, Y);
        wire D_3 = AND(Y, notZ);
        wire D_4 = AND(X, AND(notY, Z));

        wire F_1 = AND(notY, notZ);
        wire F_2 = AND(X, notY);
        wire F_3 = AND(X, notZ);

        wire G_1 = AND(X, notY);
        wire G_2 = AND(notX, Y);
        wire G_3 = AND(Y, notZ);

        // 1. Propagate wire values through combinatorial logic
        
        // Next State Logic for Modulo-10 Counter (0 to 9, then wrap to 0)
        Z1 = notZ; 
        Y1 = AND(OR(AND(Y, notZ), AND(notY, Z)), notW); 
        X1 = OR(AND(X, NOT(yz)), AND(notX, yz));        
        W1 = OR(AND(X, yz), AND(W, notZ));              

        // 7-segment display logic for digits 0-9 (Standard boolean equations)
        A = OR(OR(W, Y), OR(AND(X, Z), AND(notX, notZ)));
        B = OR(notX, OR(AND(notY, notZ), yz));
        C = OR(X, OR(notY, Z));
        D = OR(W, OR(OR(D_1, D_2), OR(D_3, D_4)));
        E = OR(D_1, D_3);
        F = OR(W, OR(F_1, OR(F_2, F_3)));
        G = OR(W, OR(G_1, OR(G_2, G_3)));

        // 2. Edge triggering: Lock values in the flip-flops
        b0.value = *b0.in;
        b1.value = *b1.in;
        b2.value = *b2.in;
        b3.value = *b3.in;

        *b0.out = b0.value;
        *b1.out = b1.value;
        *b2.out = b2.value;
        *b3.out = b3.value;

        // 3. End of a cycle; display output wire values
        #define PRINT(X) printf(#X " = %d; ", X)
        PRINT(A);
        PRINT(B);
        PRINT(C);
        PRINT(D);
        PRINT(E);
        PRINT(F);
        PRINT(G);
        printf("\n");
        fflush(stdout);
        sleep(1);
    }
}