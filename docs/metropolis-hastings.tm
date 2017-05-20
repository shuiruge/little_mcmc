<TeXmacs|1.99.1>

<style|generic>

<\body>
  <\hide-preamble>
    \;

    <assign||<macro|>>
  </hide-preamble>

  This documentation provides an illustration (and also a proof) of
  Metropolis-Hastings algorithm of sampling. The proof follows Metropolis et
  al (1953), but is modified and generalized in its morden face.

  <\notation>
    Let <math|x\<in\><with|math-font|cal|X>> any state of a given stochastic
    system. Let <math|p<around*|(|x|)>> denotes the target distribution to be
    mimicked. Let <math|q<around*|(|x\<rightarrow\>y|)>> (or
    <math|q<around*|(|y\|x|)>> by statistics) the proposed
    transition-distribution of Markov process from state <math|x> to
    <math|y><\footnote>
      i.e. the \Ppriori\Q in Metropolis et al (1953)
    </footnote>. Suppose, for any <math|x,y\<in\><with|math-font|cal|X>>,
    <math|q<around*|(|x\<rightarrow\>y|)>\<neq\>0> and
    <math|p<around*|(|x|)>\<neq\>0> (thus they are positive). And for
    Metropolis algorithm, <math|q<around*|(|x\<rightarrow\>y|)>=q<around*|(|y\<rightarrow\>x|)>>
    for <math|\<forall\>x,y\<in\><with|math-font|cal|X>> is supposed.
  </notation>

  <\algorithm>
    <label|algorithm: Metropolis>[Metropolis]

    #!/usr/bin/env python3

    # -*- coding: utf-8 -*-

    \;

    import random

    \;

    class MetropolisSampler:

    \ \ \ \ """

    \ \ \ \ Args:

    \ \ \ \ \ \ \ \ iterations: int

    \ \ \ \ \ \ \ \ initialize_state: (None -\<gtr\> State)

    \ \ \ \ \ \ \ \ markov_process: (State -\<gtr\> State)

    \ \ \ \ \ \ \ \ burn_in: int

    \;

    \ \ \ \ Attributes:

    \ \ \ \ \ \ \ \ accept_ratio: float

    \ \ \ \ \ \ \ \ \ \ \ \ Generated only after calling MetropolisSampler.

    \;

    \ \ \ \ Methods:

    \ \ \ \ \ \ \ \ sampling:

    \ \ \ \ \ \ \ \ \ \ \ \ Do the sampling by Metropolis algorithm.

    \;

    \ \ \ \ Remarks:

    \ \ \ \ \ \ \ \ The "State" can be any abstract class.

    \ \ \ \ """

    \;

    \;

    \ \ \ \ def __init__(self, iterations, initialize_state, markov_process,
    burn_in):

    \;

    \ \ \ \ \ \ \ \ self.iterations = iterations

    \ \ \ \ \ \ \ \ self.initialize_state = initialize_state

    \ \ \ \ \ \ \ \ self.markov_process = markov_process

    \ \ \ \ \ \ \ \ self.burn_in = burn_in

    \;

    \;

    \ \ \ \ def sampling(self, target_distribution):

    \ \ \ \ \ \ \ \ """

    \ \ \ \ \ \ \ \ Do the sampling.

    \;

    \ \ \ \ \ \ \ \ Args:

    \ \ \ \ \ \ \ \ \ \ \ \ target_distribution: (State -\<gtr\> float)

    \;

    \ \ \ \ \ \ \ \ Returns:

    \ \ \ \ \ \ \ \ \ \ \ \ list of State, with length being iterations -
    burn_in.

    \ \ \ \ \ \ \ \ """

    \;

    \ \ \ \ \ \ \ \ init_state = self.initialize_state()

    \ \ \ \ \ \ \ \ assert target_distribution(init_state) \<gtr\> 0

    \;

    \ \ \ \ \ \ \ \ chain = [init_state]

    \ \ \ \ \ \ \ \ accepted = 0

    \;

    \ \ \ \ \ \ \ \ for i in range(self.iterations):

    \;

    \ \ \ \ \ \ \ \ \ \ \ \ next_state = self.markov_process(init_state)

    \;

    \ \ \ \ \ \ \ \ \ \ \ \ alpha = target_distribution(next_state) /
    target_distribution(init_state)

    \ \ \ \ \ \ \ \ \ \ \ \ u = random.uniform(0, 1)

    \;

    \ \ \ \ \ \ \ \ \ \ \ \ if alpha \<gtr\> u:

    \;

    \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ accepted += 1

    \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ chain.append(next_state)

    \;

    \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ init_state = next_state.copy()

    \;

    \ \ \ \ \ \ \ \ \ \ \ \ else:

    \;

    \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ chain.append(init_state)

    \;

    \ \ \ \ \ \ \ \ self.accept_ratio = accepted / self.iterations

    \ \ \ \ \ \ \ \ print('accept-ratio = {0}'.format(self.accept_ratio))

    \;

    \ \ \ \ \ \ \ \ return chain[self.burn_in:]
  </algorithm>

  <\lemma>
    Define, for <math|\<forall\>x\<in\><with|math-font|cal|X>>,
    <math|J<around*|(|x|)>\<assign\><around*|{|\<forall\>s\<in\><with|math-font|cal|X>:
    p<around*|(|x|)>\<geqslant\>p<around*|(|s|)>|}>>. Let
    <math|h<rsub|i><around*|(|x|)>> the distribution of
    <math|\<forall\>x\<in\><with|math-font|cal|X>> at the <math|i>th Markov
    epoch. For any given <math|h<rsub|i>>, we have

    <\equation*>
      h<rsub|i+1><around*|(|x|)>-h<rsub|i><around*|(|x|)>=<big|int>\<mathd\>\<mu\><rsub|x><around*|(|s|)>
      <around*|[|h<rsub|i><around*|(|s|)>
      p<around*|(|x|)>-h<rsub|i><around*|(|x|)> p<around*|(|s|)>|]>,
    </equation*>

    where, for <math|\<forall\>x\<in\><with|math-font|cal|X>> given,

    <\equation*>
      \<mathd\>\<mu\><rsub|x><around*|(|s|)>\<assign\>\<mathd\>s
      q<around*|(|s\<rightarrow\>x|)><around*|[|
      <frac|\<delta\><around*|{|s\<in\>J<around*|(|x|)>|}>|p<around*|(|x|)>>+<frac|\<delta\><around*|(|s\<nin\>J<around*|(|x|)>|)>|p<around*|(|s|)>>|]>
    </equation*>

    is a measure.
  </lemma>

  <\proof>
    Directly from Metropolis algorithm, we have,

    <\eqnarray*>
      <tformat|<table|<row|<cell|h<rsub|i+1><around*|(|x|)>-h<rsub|i><around*|(|x|)>>|<cell|=>|<cell|<big|int><rsub|J<around*|(|x|)>>\<mathd\>s
      h<rsub|i><around*|(|s|)> q<around*|(|s\<rightarrow\>x|)>>>|<row|<cell|>|<cell|+>|<cell|<big|int><rsub|<with|math-font|cal|X>-J<around*|(|x|)>>\<mathd\>s
      h<rsub|i><around*|(|s|)> q<around*|(|s\<rightarrow\>x|)>
      <frac|p<around*|(|x|)>|p<around*|(|s|)>>>>|<row|<cell|>|<cell|->|<cell|<big|int><rsub|J<around*|(|x|)>>\<mathd\>s
      h<rsub|i><around*|(|x|)> q<around*|(|x\<rightarrow\>s|)>
      <frac|p<around*|(|s|)>|p<around*|(|x|)>>>>|<row|<cell|>|<cell|->|<cell|<big|int><rsub|<with|math-font|cal|X>-J<around*|(|x|)>>\<mathd\>s
      h<rsub|i><around*|(|x|)> q<around*|(|x\<rightarrow\>s|)>>>>>
    </eqnarray*>

    Since, in Metropolis algorithm, <math|q<around*|(|s\<rightarrow\>x|)>=q<around*|(|x\<rightarrow\>s|)>>
    is supposed,

    <\eqnarray*>
      <tformat|<table|<row|<cell|h<rsub|i+1><around*|(|x|)>-h<rsub|i><around*|(|x|)>>|<cell|=>|<cell|<big|int><rsub|J<around*|(|x|)>>\<mathd\>s
      \ q<around*|(|s\<rightarrow\>x|)> <around*|[|h<rsub|i><around*|(|s|)>-h<rsub|i><around*|(|x|)>
      <frac|p<around*|(|s|)>|p<around*|(|x|)>>|]>>>|<row|<cell|>|<cell|+>|<cell|<big|int><rsub|<with|math-font|cal|X>-J<around*|(|x|)>>\<mathd\>s
      q<around*|(|s\<rightarrow\>x|)> <around*|[|h<rsub|i><around*|(|s|)>
      <frac|p<around*|(|x|)>|p<around*|(|s|)>>-h<rsub|i><around*|(|x|)>|]>>>|<row|<cell|>|<cell|=>|<cell|<big|int>\<mathd\>\<mu\><rsub|x><around*|(|s|)>
      <around*|[|h<rsub|i><around*|(|s|)>
      p<around*|(|x|)>-h<rsub|i><around*|(|x|)> p<around*|(|s|)>|]>,>>>>
    </eqnarray*>

    where, for <math|\<forall\>x\<in\><with|math-font|cal|X>> given,

    <\equation*>
      \<mathd\>\<mu\><rsub|x><around*|(|s|)>\<assign\>\<mathd\>s
      q<around*|(|s\<rightarrow\>x|)><around*|[|
      <frac|\<delta\><around*|{|s\<in\>J<around*|(|x|)>|}>|p<around*|(|x|)>>+<frac|\<delta\><around*|(|s\<nin\>J<around*|(|x|)>|)>|p<around*|(|s|)>>|]>
    </equation*>

    is a measure.
  </proof>

  <\corollary>
    If <math|h<rsub|i>=p>, then <math|h<rsub|i+1>=p>.
  </corollary>

  <\theorem>
    <label|theorem: Metropolis>[Metropolis] Samples generated by algorithm
    <reference|algorithm: Metropolis> approximately obeys the target
    distribution <math|p<around*|(|x|)>>. That is, algorithm
    <reference|algorithm: Metropolis> creates a sampler of
    <math|p<around*|(|x|)>>.
  </theorem>

  <\proof>
    [Intuitive]

    Let <math|\<forall\>x<rsub|0>\<in\>\<cal-X\>> given. We have an infinite
    Markov chain generated by Metropolis algorithm starting at
    <math|x<rsub|0>>, say <math|<around*|{|x<rsub|0>,x<rsub|1>,x<rsub|2>,\<ldots\>|}>>.
    We want to prove that <math|<around*|{|x<rsub|0>,x<rsub|1>,x<rsub|2>,\<ldots\>|}>>
    obeys distribution <math|p<around*|(|x|)>>.

    Define <math|h<rsub|0>> by <math|<around*|{|x<rsub|0>,x<rsub|1>,x<rsub|2>,\<ldots\>|}>\<sim\>h>.<\footnote>
      Why consider an infinite series? Because what we want to prove is an
      asymptotic theorem, where the more <math|x<rsub|i>>, the better
      approximation to <math|h>. (This explains why burn-in is essential. If
      we have infinite size of the series, there would be no need of burn-in,
      since burn-in brings nothing different. However, if we cut the infinite
      series off, there must be some residue between
      <math|<around*|{|x<rsub|i>|}>> and <math|h>. Then asdf???
    </footnote> That is, the histogram of
    <math|<around*|{|x<rsub|0>,x<rsub|1>,x<rsub|2>,\<ldots\>|}>>, after
    normalization, can be fitted by <math|h<around*|(|x|)>>.<\footnote>
      Of course, this will not be a completely perfect fitting, if
      <math|<with|math-font|cal|X>> is a continuum, since
      <math|<around*|{|x<rsub|i>|}>> is countable, whereas
      <math|<with|math-font|cal|X>> is not.
    </footnote> (This demands that <math|<around*|{|x<rsub|i>|}>> must be
    ergodic.<\footnote>
      Or, consider a standard Gaussian distribution
      <math|N<around*|(|0,1|)>>. If, for some other reason (e.g. caused by
      Markov process), <math|x<rsub|i>> is not ergodic, say
      <math|x<rsub|i>\<gtr\>0> for <math|\<forall\>i>, then
      <math|N<around*|(|0,1|)>> cannot fit <math|<around*|{|x<rsub|i>|}>>,
      even though it should (i.e. when such reason were absent).
    </footnote> Then, <math|<around*|{|x<rsub|1>,x<rsub|2>,x<rsub|3>,\<ldots\>|}>\<sim\>h>,
    since dropping <math|x<rsub|0>> from the infinite set affects little on
    the fitting of histogram. On the other side, we shall not forget that
    <math|<around*|{|x<rsub|i>: i=0,1,\<ldots\>|}>> are generated by a Markov
    chain. Thus, the Metropolis algorithm as a Markov process brings
    <math|x<rsub|i>\<rightarrow\>x<rsub|i+1>> for
    <math|\<forall\>i\<in\>\<bbb-N\>>, s.t.
    <math|<around*|{|x<rsub|0>,x<rsub|1>,x<rsub|2>,\<ldots\>|}>\<rightarrow\><around*|{|x<rsub|1>,x<rsub|2>,x<rsub|3>,\<ldots\>|}>>.
    Let <math|h<rprime|'>> generated by Metropolis algorithm from <math|h>,
    that is, <math|h<rprime|'><around*|(|x|)>=h<around*|(|x|)>+\<Delta\>h<around*|(|x|)>>
    where <math|\<Delta\>h<around*|(|x|)>=<big|int><rsub|J<around*|(|x|)>>
    \<mathd\>s q<around*|(|s\<rightarrow\>x|)>
    <around*|[|h<around*|(|s|)>-h<around*|(|x|)>
    p<around*|(|s|)>/p<around*|(|x|)>|]>+<big|int><rsub|<with|math-font|cal|X>-J<around*|(|x|)>>\<mathd\>s
    q<around*|(|s\<rightarrow\>x|)> <around*|[|h<around*|(|s|)>
    p<around*|(|x|)>/p<around*|(|s|)>-h<around*|(|x|)>|]>>. Thus, we have
    <math|<around*|{|x<rsub|1>,x<rsub|2>,x<rsub|3>,\<ldots\>|}>\<sim\>h<rprime|'>>.
    That is, the histogram of <math|<around*|{|x<rsub|1>,x<rsub|2>,\<ldots\>|}>>,
    after normalization, can be fitted by <math|h<rprime|'><around*|(|x|)>>.
    Combining the two sides, we have <math|h<rprime|'><around*|(|x|)>\<approx\>h<around*|(|x|)>>
    for <math|\<forall\>x\<in\><with|math-font|cal|X><rprime|'>>, where
    <math|<with|math-font|cal|X><rprime|'>\<assign\>\<cup\><rsub|i=1><rsup|+\<infty\>>U<rsub|\<epsilon\>><around*|(|x<rsub|i>|)>>
    and <math|U<rsub|\<epsilon\>><around*|(|x<rsub|i>|)>> is some
    <math|\<epsilon\>>-neighbourhood of <math|x<rsub|i>\<in\><around*|{|x<rsub|1>,x<rsub|2>,\<ldots\>|}>>.
    This forces <math|\<Delta\>h<around*|(|x|)>\<approx\>0> for
    <math|\<forall\>x\<in\><with|math-font|cal|X><rprime|'>>.

    Next is to proof that <math|\<Delta\>h<around*|(|x|)>\<approx\>0\<Rightarrow\>h<around*|(|x|)>
    p<around*|(|y|)>-h<around*|(|y|)> p<around*|(|x|)>>. asdf
  </proof>

  \;

  \;

  <\eqnarray*>
    <tformat|<table|<row|<cell|h<around*|(|x|)>>|<cell|=>|<cell|<big|int>\<mathd\>s
    <around*|{|\<delta\><around*|(|s-x|)>+<frac|\<mathd\>\<mu\><rsub|x>|\<mathd\>s><around*|(|s|)>
    p<around*|(|x|)>-<big|int>\<mathd\>s \<delta\><around*|(|s-x|)><around*|[|
    <big|int>\<mathd\>\<mu\><rsub|x><around*|(|s<rprime|'>|)>
    p<around*|(|s<rprime|'>|)>|]>|}> h<around*|(|s|)>>>|<row|<cell|>|<cell|=>|<cell|<big|int>\<mathd\>s
    <around*|{|\<delta\><around*|(|s-x|)> <around*|[|1-
    <big|int>\<mathd\>\<mu\><rsub|x><around*|(|s<rprime|'>|)>
    p<around*|(|s<rprime|'>|)>|]>+p<around*|(|x|)>
    <frac|\<mathd\>\<mu\><rsub|x>|\<mathd\>s><around*|(|s|)>|}>
    h<around*|(|s|)>>>>>
  </eqnarray*>

  wherein

  <\eqnarray*>
    <tformat|<table|<row|<cell|1>|<cell|\<gtr\>>|<cell|1-
    <big|int>\<mathd\>\<mu\><rsub|x><around*|(|s<rprime|'>|)>
    p<around*|(|s<rprime|'>|)>>>|<row|<cell|>|<cell|=>|<cell|1-<big|int>\<mathd\>s<rprime|'>
    q<around*|(|s<rprime|'>\<rightarrow\>x|)><around*|[|
    <frac|\<delta\><around*|{|s<rprime|'>\<in\>J<around*|(|x|)>|}>|p<around*|(|x|)>>+<frac|\<delta\><around*|(|s<rprime|'>\<nin\>J<around*|(|x|)>|)>|p<around*|(|s<rprime|'>|)>>|]>
    p<around*|(|s<rprime|'>|)>>>|<row|<cell|>|<cell|=>|<cell|1-<big|int><rsub|J<around*|(|x|)>>\<mathd\>s<rprime|'>
    q<around*|(|s<rprime|'>\<rightarrow\>x|)>
    <frac|p<around*|(|s<rprime|'>|)>|p<around*|(|x|)>>-<big|int><rsub|<with|math-font|cal|X>-J<around*|(|x|)>>\<mathd\>s<rprime|'>
    q<around*|(|s<rprime|'>\<rightarrow\>x|)>>>|<row|<cell|>|<cell|\<gtr\>>|<cell|1-<big|int>\<mathd\>s<rprime|'>
    q<around*|(|s<rprime|'>\<rightarrow\>x|)>=0>>>>
  </eqnarray*>

  and

  <\eqnarray*>
    <tformat|<table|<row|<cell|>|<cell|>|<cell|p<around*|(|x|)>
    <frac|\<mathd\>\<mu\><rsub|x>|\<mathd\>s><around*|(|s|)>>>|<row|<cell|>|<cell|=>|<cell|q<around*|(|s\<rightarrow\>x|)><around*|[|
    \<delta\><around*|{|s\<in\>J<around*|(|x|)>|}>+\<delta\><around*|(|s\<nin\>J<around*|(|x|)>|)><frac|p<around*|(|x|)>|p<around*|(|s|)>>|]>>>|<row|<cell|>|<cell|<above|\<less\>|<around*|(|\<leqslant\>?|)>>>|<cell|q<around*|(|s\<rightarrow\>x|)>>>>>
  </eqnarray*>

  Thus, the ``kernel''

  <\eqnarray*>
    <tformat|<table|<row|<cell|>|<cell|>|<cell|\<delta\><around*|(|s-x|)>
    <around*|[|1- <big|int>\<mathd\>\<mu\><rsub|x><around*|(|s<rprime|'>|)>
    p<around*|(|s<rprime|'>|)>|]>+p<around*|(|x|)>
    <frac|\<mathd\>\<mu\><rsub|x>|\<mathd\>s><around*|(|s|)>>>|<row|<cell|>|<cell|\<in\>>|<cell|<around*|(|0,\<delta\><around*|(|s-x|)>+q<around*|(|s\<rightarrow\>x|)>|)>>>>>
  </eqnarray*>

  In the same way,

  <\eqnarray*>
    <tformat|<table|<row|<cell|0>|<cell|=>|<cell|<big|int>\<mathd\>s
    <around*|{|<frac|\<mathd\>\<mu\><rsub|x>|\<mathd\>s><around*|(|s|)>
    p<around*|(|x|)>-<big|int>\<mathd\>s \<delta\><around*|(|s-x|)><around*|[|
    <big|int>\<mathd\>\<mu\><rsub|x><around*|(|s<rprime|'>|)>
    p<around*|(|s<rprime|'>|)>|]>|}> h<around*|(|s|)>>>|<row|<cell|>|<cell|=>|<cell|<big|int>\<mathd\>s
    <around*|{|\<delta\><around*|(|s-x|)> <around*|[|-
    <big|int>\<mathd\>\<mu\><rsub|x><around*|(|s<rprime|'>|)>
    p<around*|(|s<rprime|'>|)>|]>+p<around*|(|x|)>
    <frac|\<mathd\>\<mu\><rsub|x>|\<mathd\>s><around*|(|s|)>|}>
    h<around*|(|s|)>>>|<row|<cell|>|<cell|=>|<cell|<big|int>\<mathd\>s
    K<around*|(|x,s|)> h<around*|(|s|)>>>>>
  </eqnarray*>

  wherein

  <\eqnarray*>
    <tformat|<table|<row|<cell|K<around*|(|x,s|)>>|<cell|=>|<cell|\<delta\><around*|(|s-x|)>
    <around*|[|-<big|int><rsub|J<around*|(|x|)>>\<mathd\>s<rprime|'>
    q<around*|(|s<rprime|'>\<rightarrow\>x|)>
    <frac|p<around*|(|s<rprime|'>|)>|p<around*|(|x|)>>-<big|int><rsub|<with|math-font|cal|X>-J<around*|(|x|)>>\<mathd\>s<rprime|'>
    q<around*|(|s<rprime|'>\<rightarrow\>x|)>|]>>>|<row|<cell|>|<cell|+>|<cell|q<around*|(|s\<rightarrow\>x|)><around*|[|
    \<delta\><around*|{|s\<in\>J<around*|(|x|)>|}>+\<delta\><around*|{|s\<nin\>J<around*|(|x|)>|}>
    <frac|p<around*|(|x|)>|p<around*|(|s|)>>|]>>>>>
  </eqnarray*>

  where

  <\equation*>
    -1\<less\> <around*|[|-<big|int><rsub|J<around*|(|x|)>>\<mathd\>s<rprime|'>
    q<around*|(|s<rprime|'>\<rightarrow\>x|)>
    <frac|p<around*|(|s<rprime|'>|)>|p<around*|(|x|)>>-<big|int><rsub|<with|math-font|cal|X>-J<around*|(|x|)>>\<mathd\>s<rprime|'>
    q<around*|(|s<rprime|'>\<rightarrow\>x|)>|]>\<less\>0
  </equation*>

  and

  <\equation*>
    0\<less\><around*|[| \<delta\><around*|{|s\<in\>J<around*|(|x|)>|}>+\<delta\><around*|{|s\<nin\>J<around*|(|x|)>|}>
    <frac|p<around*|(|x|)>|p<around*|(|s|)>>|]>\<leqslant\>
    \<delta\><around*|{|s\<in\>J<around*|(|x|)>|}>+\<delta\><around*|{|s\<nin\>J<around*|(|x|)>|}>
  </equation*>

  \;

  asdf
</body>

<initial|<\collection>
</collection>>

<\references>
  <\collection>
    <associate|algorithm: Metropolis|<tuple|1|?>>
    <associate|footnote-1|<tuple|1|?>>
    <associate|footnote-2|<tuple|2|?>>
    <associate|footnote-3|<tuple|3|?>>
    <associate|footnote-4|<tuple|4|?>>
    <associate|footnr-1|<tuple|1|?>>
    <associate|footnr-2|<tuple|2|?>>
    <associate|footnr-3|<tuple|3|?>>
    <associate|footnr-4|<tuple|4|?>>
    <associate|theorem: Metropolis|<tuple|4|?>>
  </collection>
</references>