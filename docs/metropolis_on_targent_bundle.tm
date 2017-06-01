<TeXmacs|1.99.1>

<style|generic>

<\body>
  Let <math|X> space of state, and <math|TB<around*|(|X|)>> the targent
  bundle of <math|X>. For any space <math|S>, let <math|E<around*|(|S|)>> the
  esemble of <math|S>. For <math|\<forall\>q\<in\>X>, denote
  <math|r=<around*|(|p,q|)>\<in\>TB<around*|(|X|)>>. And for
  <math|\<forall\>Q\<in\>E<around*|(|X|)>>, denote
  <math|R=<around*|(|P,Q|)>\<in\><around*|(|E\<circ\>TB|)><around*|(|X|)>>.

  To gain a MCMC, we shall for some <math|\<pi\><around*|(|R|)>\<in\>Map<around*|{|<around*|(|E\<circ\>TB|)><around*|(|X|)>,\<bbb-R\>|}>>
  given, and some <math|J<around*|(|R,R<rprime|'>|)>\<in\>Map<around*|{|<around*|(|E\<circ\>TB|)><rsup|2><around*|(|X|)>,\<bbb-R\>|}>>
  given, construct <math|K<around*|(|R,R<rprime|'>;\<pi\>,J|)>\<in\>Map<around*|{|<around*|(|E\<circ\>TB|)><rsup|2><around*|(|X|)>,\<bbb-R\><rsup|+>|}>>,
  s.t.

  <\equation*>
    <big|sum><rsub|R>\<pi\><around*|(|R|)>
    K<around*|(|R,R<rprime|'>|)>=\<pi\><around*|(|R<rprime|'>|)>.
  </equation*>

  Or, at least,

  <\equation*>
    \<pi\><around*|(|R|)> K<around*|(|R,R<rprime|'>|)>=\<pi\><around*|(|R<rprime|'>|)>
    K<around*|(|R<rprime|'>,R|)>.
  </equation*>
</body>

<initial|<\collection>
</collection>>