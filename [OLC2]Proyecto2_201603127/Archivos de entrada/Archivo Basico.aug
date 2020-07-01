main:

    $t1 = 0; #PUNTEO

    print("-------------ARCHIVO BASICO---------------");
    print("\n");
    print("-------------DECLARACION-------------\n");
    $t2 = 0;
    $t3 = $t2;
    $t4 = 2;
    $t5 = "Compiladores 2 Junio 2020";
    $t6 = "s";
    if ( $t2 == $t3 ) goto siP1;
    print( "Problemas con la declaración de variables :c" );
    print("\n");
    goto finP1;
siP1:
    print($t5);
    print("\n");
    print($t6);
    print("\n");
    print(" ");
    print($t4);
    print("\n");
    $t1 = $t1 + 1;
finP1:
    print("\n-------------CONCATENACION-------------");
    print("\n");
    $t7 = "Hola ";
    $t8 = $t7 + "C";
    $t9 = $t8 + "O";
    $t10 = $t9 + "M";
    $t11 = $t10 + "P";
    $t12 = $t11 + "I";
    print($t12);
    print("\n");
    if ( $t12 == "Hola COMPI" ) goto siP2;
    print(" Concateno mal :( ");
    goto finP2;
siP2:
    print("Contatenacion de String Nice.");
    $t1 = $t1 + 1;
finP2:
    print("\n");
    print("-------------SUMA VARIABLES-------------");
    print("\n");
    $t13 = 0.0;
    $t14 = $t13 + 1;
    $t15 = $t14 + 1;
    $t16 = $t15 + 1;
    $t17 = $t16 + 0.1;
    $t18 = $t17 + 49;
    print($t18);
    print("\n");
    if ( $t18 == 52.1 ) goto siP3;
    print(" Sumo mal :( \n");
    goto operacionesBasicas;
siP3:
    print("Suma de enteros y decimales \n");
operacionesBasicas:
    print("\n");
    print("Operaciones Aritmeticas 1: valor esperado: ");
    print("\n");
    print("a)62");
    print("\n");
    print("b)0");
    print("\n");
    print("c)-19");
    print("\n");
    print("d)256");
    print("\n");
    print("resultados:");
    print("\n");
    $t19 = 8/2;
    $t20 = $t19 * 3;
    $t21 = $t20 + 20;
    $t22 = $t21 - 10;
    $t23 = $t22 + 10;
    $t24 = $t23 - 10;
    $t25 = $t24 - 10;
    $t26 = $t25 + 50; #VALOR DE A
    $t27 = 50/50;
    $t28 = $t27 * 50;
    $t29 = $t28 + 50;
    $t30 = $t29 - 100;
    $t31 = $t30 + 100;
    $t32 = $t31 - 100; #VALOR DE B
    $t33 = 100 / 20;
    $t34 = $t33 * 9;
    $t35 = $t34 - 78;
    $t36 = $t35 + 6;
    $t37 = $t36 - 7;
    $t38 = $t37 + 8;
    $t39 = $t38 - 7;#
    $t40 = 7 * 1;
    $t41 = $t40 * 2;
    $t42 = $t41 * 3;
    $t43 = $t42 / 3;
    $t44 = $t39 + $t43; #VALOR DE C
    $t45 = (int) $t26;
    $t46 = (int) $t32;
    $t47 = (int) $t44;
    print("a) ");
    print($t45);
    print("\n");
    print("b) ");
    print($t46);
    print("\n");
    print("c) ");
    print($t47);
    print("\n");
    if ( $t45 != 62 ) goto mal1;
    if ( $t46 != 0 ) goto mal1;
    $t48 = -19;
    if ( $t47 != $t48 ) goto mal1;
    print("Operaciones aritmeticas bien.\n");
    $t1 = $t1 + 2;
    goto operacionesLogicas;
mal1:
    print("Error Operaciones Aritmeticas\n");
operacionesLogicas:
    print("-------------LOGICAS 1-------------\n");
    $t45 = 1;
    $t46 = !$t45;
    $t47 = !$t46; 
    $t48 = !$t47;
    $t49 = !$t48;
    $t50 = !$t49;
    if ( $t50 != 0 ) goto mal2;
    print("NOT bien.");
    goto OL2;
mal2:
    print("Error NOT");
OL2:
    print("\n");
    print("-------------LOGICAS 2-------------");
    print("\n");
    $t51 = 1 && 1;
    $t52 = 0 && 0;
    $t53 = $t52 && 0;
    $t54 = !1;
    $t55 = $t51 || $t53;
    if ( $t55 || $t54 ) goto siOL2;
    print("Mal AND, OR, XOR, NOT \n");
    goto BB;
siOL2:
    if ( $t51 xor $t52 ) goto siOL3;
    print("Mal AND, OR, XOR, NOT \n");
    goto BB;
siOL3:
    print("Bien AND, OR, XOR, NOT \n");
    $t1 = $t1 + 2;
BB:
    print("\n");
    print("-------------BIT A BIT-------------");
    print("\n");
    $t56 = 5 | 6;
    $t57 = $t56 & 10;
    $t58 = ~49;
    $t59 = 20 ^ 60;
    $t591 = 3 << 6;
    $t592 = 65 >> 3;
    print($t56);
    print("\n");
    print($t57);
    print("\n");
    print($t58);
    print("\n");
    print($t59);
    print("\n");
    print($t591);
    print("\n");
    print($t592);
    print("\n");
    if ( $t56 != 7 ) goto mal3;
    if ( $t57 != 2 ) goto mal3;
    if ( $t58 != -50 ) goto mal3;
    if ( $t59 != 40 ) goto mal3;
    if ( $t591 != 192) goto mal3;
    if ( $t592 != 8) goto mal3;
    print("Bien BIT A BIT \n");
    $t1 = $t1 + 2;
    goto OR1;
mal3:
    print("Mal BIT A BIT");
OR1:
    print("\n");
    print("-------------RELACIONALES 1-------------");
    print("\n");
    $t60 = 34 + 0.0;
    if ( $t60 < 34.44 ) goto bien1;
    goto mal4;
bien1:
    $t60 = $t60 + 15;
    if ( $t60 > 44 ) goto bien2;
    goto mal5;
bien2:
    $t60 = $t60 + 1;
    goto segunda;
mal5:
    $t60 = 1;
    goto segunda;
mal4:

segunda:
    if( $t60 != 1 ) goto bien3;
    goto mal6;
bien3:
    if( $t60 == 50 ) goto bien4;
mal6:
    print("Salida incorrecta!\n");
    goto finR1;
bien4:
    print("SALIDA CORRECTA!");
    $t1 = $t1 + 1;
finR1:
    print("\n");
OR2:
    print("-------------RELACIONALES 2-------------");
    print("\n");
    $t61 = 10 - 15;
    $t62 = $t61 >= 0;
    $t63 = 44.44 == 44.44;
    if( $t62 && $t63 ) goto mal7;
    
    $t64 = 15 + 8;
    $t65 = 22 - 10;
    $t66 = 5 * 3;
    $t67 = $t65 + $t66;
    $t68 = $t67 - 4;
    $t69 = $t64 == $t68;
    $t70 = 13 * 0;
    $t71 = -1;
    $t72 = $t70 > $t71;
    if( $t69 && $t72 ) goto bien5;
    goto mal7;
bien5:
    $t73 = 10.0;
    $t74 = 11.1 - 1.01;
    $t75 = $t73 != $t74;
    if( $t75 ) goto bien6;
mal7:
    print("RELACIONALES 2 INCORRECTA.\n");
    goto fintotal;
bien6:
    print("RELACIONALES 2 CORRECTAS.\n");
    $t1 = $t1 + 1;
fintotal:
    print("\n");
    print("PUNTEO TOTAL: ");
    print($t1);