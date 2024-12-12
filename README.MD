The following is my short essay on optimization:
For this project I struggled to optimize very well past my first effort at translating the pseudocode into real code.
I found that it took only two seconds to run my stochastic pagerank when running it with 100,000 steps, 1,000 times the default amount and that at the default amount, it ran instantaneously.
As for my stochastic pagerank, it still only took 0.12-0.15 seconds for the default one hundred steps amount which I found to be very quick.
The ways in which I believe my stochastic pagerank code is optimized are in that how I used a dictionary for hit_count which allowed for real time updates to record node visit counts.
Another way is in the fact that I made efficient pythons built-in random function which both allowed for efficient coding but also for the algorithm to quickly access randomly chosen nodes, allowing for the pagerank algorithm to be performed quicker.
One way is efficient use of memory management. What I mean by this is that there isn't too many variables being stored at once as only hit_count and current_node are being used. By wasting as little memory as possible, the load on the computer is lower and therefore allows for the program to run faster.
On the topic of memory management, nodes with no outgoing edges are effectively dealt with as they are immediately redirected to a new random node which avoids as much memory wastage as possible.
As for the distribution pagerank, there are similar themes such as few stored variables, dead end nodes dealt with effectively.
Additionally, like using random for efficient random node choosing, the dictionary usage allows for efficient node access which allows for a quick pagerank algorithm.

While these are reasons for why they run efficiently, another important step was implementing the timing of the functions and the progress bar to allow me to understand how efficiently the code is running and if changes improve or slow algorithm times.

Overall, I am happy with the efficiency of the algorithms I have worked on and also the skills I have developed.