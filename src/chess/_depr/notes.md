

## Informationen regelklassen behöver för att veta om ett drag är lagligt eller ej


- Vems drag är det (w/b)
- Vilken pjäs flyttas och var
- Var spelarens kung i schack (pre move)? 
- Hamnar spelarens kung i schack (post move, .copy())




## Information som brädesklassen bör ha koll på 

Skapa dict som håller koll på:
- vems tur det är att göra ett drag / hur mågna drag som gjorts
- antal drag utan 'capture' - 50 move rule
- rättigheter till rokad - påverkas av: torn som flyttats, kung som flyttats, pjäster i vägen, attackerade rutor/schack
- ...en passent?? 



## I rules klassen 
- skapa pre-move och post-move bräden som former av boardstates. Uppdatera boardstate till postmove endast om draget är lagligt. 
- i brädesklassen: skapa dict med historik över alla drag (kolla formell notation)



## Formell notation för schackdrag:
PGN (portable game notation)

- move: 
    - pawn move: the square coord (e.g. d4)
    - pawn promotion: (e.g. e8=Q, e8(Q) or e8/Q)
    - capture: with an x inbetween piece and square (e.g. Qxc4)
    - castle: 
    - check: + (doublecheck with ++ )
    - checkmate: x or X

1. e4 e5
2. Nf3 Nc6
3. Bb5 a6
4. etc.

Ambigious situations:
- two rooks on same file (R1a3 or R5a3, the first number indicating the rank of the piece, same can be done for diagonal moves)
- nights are tricky, might need indication of which file or rank they came from (check if two or nore nights can make the move)
- NOTE or just use own notation where from_coord is explicitly recorded each move (no ambiguity then)

- at the the end of openening {comment about opening name} can be inserted (after move, e.g. ... 3. Bb5 a6 {Ruy Lopez opening})
https://en.wikipedia.org/wiki/Portable_Game_Notation 

King:   K
Queen:  Q
Bishop: B
Night:  N
Rook:   R
Pawn:   . (only square)
