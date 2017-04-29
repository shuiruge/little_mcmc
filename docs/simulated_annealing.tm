<TeXmacs|1.99.1>

<style|generic>

<\body>
  Let <math|E<around*|(|x|)>> any target function. We are aiming to get the
  <math|argmin<around*|{|E<around*|(|x|)>|}>>.

  If let <math|p<around*|(|x|)> = exp<around*|(|-E<around*|(|x|)>/T|)>>, then
  in Metropolis algorithm, <math|acceptence =
  p<around*|(|x<rsub|i+1>|)>/p<around*|(|x<rsub|i>|)>\<gtr\>u\<Rightarrow\>exp<around*|(|-<around*|(|E<around*|(|x<rsub|i+1>|)>-E<around*|(|x<rsub|i>|)>|)>/T|)>\<gtr\>u>,
  where <math|u=random.uniform<around*|(|0, 1|)>>. This is just the same as
  simulated anealing algorithm (c.f. <hlink|here|http://mathworld.wolfram.com/SimulatedAnnealing.html>).
  That is, to minimize any function <math|E<around*|(|x|)>>, we only need to
  construct a target distribution for Metropolis sampler, i.e. the
  <math|p<around*|(|x|)>>. Then, we can get the eagered
  <math|argmin<around*|{|E<around*|(|x|)>|}>> directly from Metropolis
  sampler.
</body>

<initial|<\collection>
</collection>>