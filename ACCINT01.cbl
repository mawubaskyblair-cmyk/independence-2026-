IDENTIFICATION DIVISION.
       PROGRAM-ID. ACCINT01.
       AUTHOR. CORE-BANKING-TEAM.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ACCOUNT-FILE ASSIGN TO "ACCTFILE.DAT"
               ORGANIZATION IS INDEXED
               ACCESS MODE IS SEQUENTIAL
               RECORD KEY IS ACCT-ID.

       DATA DIVISION.
       FILE SECTION.
       FD  ACCOUNT-FILE.
       01  ACCOUNT-RECORD.
           05 ACCT-ID            PIC 9(10).
           05 ACCT-BALANCE       PIC S9(13)V99 COMP-3.
           05 ACCT-RATE          PIC 9(02)V9999 COMP-3.
           05 ACCT-TYPE          PIC X(01).

       WORKING-STORAGE SECTION.
       01  WS-INTEREST-CALC     PIC S9(13)V99 COMP-3 VALUE ZERO.
       01  WS-DAILY-RATE        PIC 9(02)V99999999 COMP-3 VALUE ZERO.
       01  WS-EOF-FLAG          PIC X(01) VALUE 'N'.

       PROCEDURE DIVISION.
       0000-MAIN-LOGIC.
           OPEN I-O ACCOUNT-FILE.
           PERFORM UNTIL WS-EOF-FLAG = 'Y'
               READ ACCOUNT-FILE NEXT RECORD
                   AT END
                       MOVE 'Y' TO WS-EOF-FLAG
                   NOT AT END
                       PERFORM 1000-CALCULATE-INTEREST
               END-READ
           END-PERFORM.
           CLOSE ACCOUNT-FILE.
           STOP RUN.

       1000-CALCULATE-INTEREST.
           IF ACCT-BALANCE > ZERO THEN
               COMPUTE WS-DAILY-RATE = ACCT-RATE / 365
               COMPUTE WS-INTEREST-CALC ROUNDED = 
                   ACCT-BALANCE * WS-DAILY-RATE
               ADD WS-INTEREST-CALC TO ACCT-BALANCE
               REWRITE ACCOUNT-RECORD
           END-IF.