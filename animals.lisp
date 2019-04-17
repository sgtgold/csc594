#| File is: ANIMAL.LISP  ---  Clark Elliott  version 7.2  2019-04-03

1. Alter the program so that it prints out YOUR NAME when it starts up.

2. Alter the program so that it has additional gloating and I-lost responses.

3. Write three additional functions:
   A. (make-normal-personality)
   B. (make-depressed-personality)
   C. (make-manic-personality)

Here are some depressed winning responses:

"I'm usually wrong, but got that right."
"For once I guess I'm right."
"I'm sorry I am the winner."

Here are some depressed losing responses:

"Yes I expected to lose."
"I always do lose. It is normal for me."
"I’m glad I am the loser. I deserve it."

Your depressed personality should exhibit such depressed winning and losing responses.

Ditto for the manic and normal personalities.

To show your work, you can use the lisp (dribble "MyFile.txt") function:

   LISP> (dribble "MyRunningAnimal.txt") <-- This opens the DRIBBLE file of that name

   [run your program] <-- show us what your program can do.

   LISP> (dribble) <-- This closes the file which is now in your directory

You now have documentation of your running program to submit to D2L

;;;-----------------------------------------------------------------

More advanced:

For the more advanced version of the Animal program, the more times the program gets wrong
answers, the more intense its emotions get. The more times the program gets right answers, the
less intense its emotions get.

Develop a model of the intensity of its responses that will work with any one of the
personalities. (You will need to create more response sets -- one for each level of intensity
you model.)

You might need:

LISP> (setf *intensity* 10)
LISP> 10
LISP> (incf *intensity*)
11

*intensity* is now equal to 11. The same as (setf *intensity* (+ *intensity* 1))

(decf *intensity*)
10

*intensity* is now equal to 10 again.

In this way we begin to model the real-time, reponsive emotion state of the
game.

For fun, you can also cause *intensity* to be written to disk and reloaded
when you reload the data. Now we are starting to build an "agent" that
maintains state.

;;;-----------------------------------------------------------------

Super bragging rights:


Develop a more sophisticate model of the game agent's emotions that operate on different emotions. For example how might it develop:

ADMIRATION for you (the user) for doing the right thing.

Right thing: guessing correctly? Playing again? other...?

ANGER at you because you have done the wrong thing (x) and blocked its goals (y)

Wrong thing: what simple principles might the game-agent have that you have
violated?

What goals of the game-agent might you have blocked through your actions?

GRATITUDE toward you because you have done the right thing (p) and helped it achieve one of its goals (q)

How might it develop a friendship or adversarial relationship with you?

Being HAPPY-FOR you because it believes you have gotten something you (its friend) want?
Being RESENTFUL of you because it believes you have gotten something you (its adversary) want?
Being SORRY-FOR you because it believes you have lost something you (its friend) want to keep?
GLOATING over you because it believes you have lost something you (its adversary) want to keep?

ETC.

see https://condor.depaul.edu/elliott/ar/papers/EmotionTable2016.html

;;;-----------------------------------------------------------------

Here is what a saved data file a.lisp looks like (indentation added):

(setq
 *nodes*
 '(
   (3 "Does it have antennae" ANT LIZARD)
   (2 "Does it have a bushy tail" FOX COW)
   (THING "Is this thing a mammal" (2) (3))
   ))
(setq *node-count* 3)

;;;-----------------------------------------------------------------


Be sure to make periodic backups of your work:

> Copy AnimalB.lisp save-Animal-B.lisp

And keep versions:

> Copy AnimalB.lisp AnimalC.lisp


Run this in Armed Bear Common LISP that runs under java:

> java -jar abcl-0.15.0.jar
> (load "animal.lisp")

> (load "animal") <-- this shorthand will also work.

This program tries to guess what animal you are thinking of by
asking questions. If it guesses wrong, it will learn the correct answer
for next time. It uses a dynamically constructed binary search tree.

To save a session, after answering "n" to "Do you want to play again?,"
type (saveit "filename.lisp") where filename is the name of the file into
which you wish to save your data (e.g., (saveit "a.lisp") (saveit "b.lisp").

WARNING!! Be sure you don't save your data file on top of your LISP program:

No, no, no! ==> (saveit "animal.lisp") NO, NO!

To load your data back in, type (load "filename.lisp") where filename is the
name of the file in which your data resides

If you have much data (many animals) save copies of your data file (which might get corrupted):

> Copy b.lisp save-b.lisp

Run the program, play with it, then make the modifications specified in the assignment.

Add your extensive COMMENTS about what the program is doing in each section of the code.

|#

;;; HERE IS WHERE YOU ADD CODE TO PRINT YOUR NAME USING THE FORMAT COMMAND:

(format t "~%This is Jacob Penrod's Animal Learning program~%")
;Set a default state for the program
(setq curr-state "new")
;Create empty lisp files if they exist
(open "state.lisp" :if-does-not-exist :create) 
(open "MyAnimalData.lisp" :if-does-not-exist :create) 
;Loading past state
(format t "Remembering our previous encounters~%")
;default values that maybe overriden by the load of state.lisp
(setq *intensity* 10)
(setq *n-wins* 0)
(setq *n-lose* 0)
(setq *n-norm-wins* 0)
(setq *n-norm-lose* 0)
(setq *n-dep-wins* 0)
(setq *n-dep-lose* 0)
(setq *n-manic-wins* 0)
(setq *n-manic-lose* 0)

(load "state.lisp")
(load "MyAnimalData.lisp")

;This puts guessing program in a normal state (when intensity is between 8 and 12)
(defun make-normal-personality () 
	(setq curr-state "normal")
	
	(setq *normal-win-responses*
		  (list "Woot!"
				"I thought so"
				"Hah, you cannot fool me!"
				"Hurray for me!")
	)

	(setq *normal-lose-responses*
		  (list "I'll do better next time"
				"Ahh -- nuts."
				"Rats, I thought I knew that one"
				"Fooey, I will get you next time")
	)
	(setq *win-responses* *normal-win-responses*)
	(setq *lose-responses* *normal-lose-responses*)

)
;This puts guessing program in a depressed state (when intensity is less than 8)
(defun make-depressed-personality ()  
	(setq *depressed-win-responses*
		  (list "I'm usually wrong, but got that right."
				"For once I guess I'm right."
				"I'm sorry I am the winner."))
	(setq *depressed-lose-responses*
      (list "Yes I expected to lose."
			"I always do lose. It is normal for me."
			"I’m glad I am the loser. I deserve it."
			))
	(setq curr-state "depressed")
	(setq *win-responses* *depressed-win-responses*)
	(setq *lose-responses* *depressed-lose-responses*)

)
;This puts guessing program in a manic state (when intensity is greater than 12)
(defun make-manic-personality ()  
	(setq *manic-win-responses*
		  (list "Can we increase the bet?"
				"Let the good times roll!"
				"I'm the best at this game!"))
	(setq *manic-lose-responses*
      (list "I bet I'll win next time"
			"My luck is bound to turn around soon!"
			"That's only one time, I'm sure I'll win soon."
			))
	(setq curr-state "manic")
	(setq *win-responses* *manic-win-responses*)
	(setq *lose-responses* *manic-lose-responses*)
)


; Welcome back messages
(if (string= curr-state "normal")
	(progn (format t "Welcome Back~%") (make-normal-personality))
)
(if (string= curr-state "depressed")
	(progn (format t "Oh, you're back. I'll probably lose~%") (make-depressed-personality))
)
(if (string= curr-state "manic")
	(progn (format t "Welcome back, I'm going to win big this time!~%") (make-manic-personality))
)
(if (string= curr-state "new")
	(progn (format t "Welcome new friend!~%") (make-normal-personality))
)
;;; ABOVE IS WHERE YOU ADD CODE TO PRINT YOUR NAME USING THE FORMAT COMMAND.

(setq *n-games* 0)
(defun animal () 
  (loop
   (incf *n-games*)
   (run-node 'thing)
    (when (not (ask-play-again)) 
      (format t "Thanks for playing. [Use (saveit \"fname.lisp\") ~
                 if you want to save your data.]~%")
      (return)
	)
	(save-state "state.lisp")
	(saveit "MyAnimalData.lisp")
	)
)

;;; =============================================================
;;; ======   This is the section we will modify:   ==============
;;; =============================================================
;;; Information about user history, not all of these are used, but I feel they could be in 
;;; future implementations


;;; Note that the *win-responses* and *lose-responses* are important in completing this assignment.

;;; HERE ARE THREE OF THE FUNCTIONS YOU MUST WRITE:
;;; Replace the "t" with program code in each function.


;Winning function which can also change mood
(defun gloat ()
  
	(if (string= curr-state "normal")
		(incf *n-norm-wins*) 
	)
	(if (string= curr-state "depressed")
		(incf *n-dep-wins*) 
	)
	(if (string= curr-state "manic")
		(incf *n-manic-wins*) 
	)
	(incf *n-wins*)
	(incf *intensity*)
	(if (and (> *intensity* 12) (string/= curr-state "manic" ))(progn(format t "All I do is win, win, win!.~%") (make-manic-personality))
	)
	(if (and (and (>= *intensity* 8) (< *intensity* 12)) (string/= curr-state "normal"))(progn (format t "Getting back in the swing of things~%") (make-normal-personality))
	)
	(let ((i (random (length *win-responses*))))
    (format t "~A~%" (nth i *win-responses*)))
	
)

;Losing function which can also change mood
(defun i-lost ()
 	(if (string= curr-state "normal")
		(incf *n-norm-lose*) 
	)
	(if (string= curr-state "depressed")
		(incf *n-dep-lose*) 
	)
	(if (string= curr-state "manic")
		(incf *n-manic-lose*) 
	)
	;Increment state variables
	(incf *n-lose*)
	(decf *intensity*)
	;Change EIA state to normal
	(if (and ( and (< *intensity* 12) (> *intensity* 8) (string/= curr-state "normal" )))
		(progn(format t "Even though I'm losing, I'm enjoying our time together.~%") (make-normal-personality))
	)
	;Change EIA state to depressed
	(if (and (<= *intensity* 8) (string= curr-state "normal" ))
		(progn(format t "**sigh** Fine, I guess I'll play again ~%") (make-depressed-personality))
	)
	(let ((i (random (length *lose-responses*))))
    (format t "~A~%" (nth i *lose-responses*)))

)

; Save off state data for the program
(defun save-state (filename)
  (if (stringp filename)
      (let ((saver (open filename :direction :output 
			 :if-exists :supersede)))
			(format saver "(setq *intensity* ~s)" *intensity*)
			(format saver "(setq *n-games* ~s)" *n-games*)
			(format saver "(setq curr-state ~s)" curr-state)
			(format saver "(setq *n-wins* ~s)" *n-wins*)
			(format saver "(setq *n-lose* ~s)" *n-lose*)
			(format saver "(setq *n-norm-wins* ~s)" *n-norm-wins*)
			(format saver "(setq *n-norm-lose* ~s)" *n-norm-lose*)
			(format saver "(setq *n-dep-wins* ~s)" *n-dep-wins*)
			(format saver "(setq *n-dep-lose* ~s)" *n-dep-lose*)
			(format saver "(setq *n-manic-wins* ~s)" *n-manic-wins*)
			(format saver "(setq *n-manic-lose* ~s)" *n-manic-lose*)
			(close saver)
		)	
    (format t "Sorry, filename must be a string~%")))

;;; ABOVE ARE THE FUNCTIONS YOU MUST WRITE.


;;; =============================================================
;;; ======+++   End of what we will modify  =====================
;;; =============================================================


(defun saveit (filename)
  (if (stringp filename)
      (let ((saver (open filename :direction :output 
			 :if-exists :supersede)))
	(format saver "(setq *nodes* ~%'")
	(pprint *nodes* saver) ; Save our database of animals to a file.
	;(format saver "~%(setq *nodes* '~s)" *nodes*)
	(format saver ")~%(setq *node-count* ~s)" *node-count*)
        (close saver)) ; note SHOULD use with-open-file, not in XLISP
      (format t "Sorry, filename must be a string~%")))

(defvar *nodes*) (setq *nodes* nil)
(defvar *node-count*) (setq *node-count* 1)
(defun node-count () (incf *node-count*))

(defun node-name (n)       (first n))
(defun node-question (n)   (second n))
(defun node-yes-branch (n) (third n))
(defun node-no-branch (n)  (fourth n))

(defun defnode (name question yes-branch no-branch)
  (setq *nodes* 
	(cons (list name question yes-branch no-branch) *nodes*)))

(defnode 'thing "Is this thing a mammal" 'cow 'lizard)
;;; I encourage you to use other data sets instead. For example:
;;; (defnode 'thing "Is this car fast" 'ferrari 'yugo)
;;; (defnode 'thing "Does this sport have a round ball" 'basketball 'football)

(defun get-node (name)  (assoc name *nodes*))

(defun run-node (name)
  (let ((n (get-node name)) (response nil))
    (if (equal (ask (node-question n)) 'y)

	(if (symbolp (node-yes-branch n))
	    (if (guess (node-yes-branch n))
		(gloat)
	        (setf (rest n)
		      (list (second n) (add-node (node-yes-branch n))
			    (fourth n)))) ; hack around xlisp shortcomming.
	    (run-node (first (node-yes-branch n))))

	(if (symbolp (node-no-branch n))
	    (if (guess (node-no-branch n))
		(gloat)
	        (setf (rest n)
		      (list (second n) (third n)
			    (add-node (node-no-branch n)))))
	    (run-node (first (node-no-branch n)))))))

(defun ask (question) 
  (format t "~a? [y/n]~%" question)
  (read))

(defun add-node (answer-tried)
  (let ((new-thing nil) (new-node-name (node-count)) (new-node nil))
    (i-lost)
    (format t "~%What was it [type one word]?~%")
    (setq new-thing (read))
    (format t 
	    "Type a question that is true for ~s ~
             and false for ~s [in quotes]:~%~%"
	    new-thing answer-tried)
    (defnode new-node-name (read) new-thing answer-tried) ; read-line problem
    (list new-node-name)))

(defun ask-play-again ()
  (format t "~%Would you like to play again? [y/n]~%")
  (equal (read) 'y))

(defun guess (name)
  (format t "Is it a ~s? [y/n]~%" name)
  (equal (read) 'y))

(format t "~%To read in previous data [in MyData.lisp], ")
(format t "type (load \"MyData.lisp\") at the LISP prompt.~%~%")
(format t "To play animal, just type (animal) at the LISP prompt~%~%")