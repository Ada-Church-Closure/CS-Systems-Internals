(define (square n) (* n n))

(define (pow base exp) 
  (if (or (= base 1) (= exp 0)) 
    1
    (* base (pow base (- exp 1))))
)

(define (repeatedly-cube n x)
  (if (zero? n)
      x
      (let ((y (* x x x)))
        (repeatedly-cube (- n 1) y))))

(define (cddr s) (cdr (cdr s)))

(define (cadr s) 
  (car (cdr s))
)

(define (caddr s) 
  (car (cdr (cdr s)))
)
