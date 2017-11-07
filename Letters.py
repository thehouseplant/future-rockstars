print ("Generate Acceptance/Rejection letter here:")
firstName= input("First Name:")
lastName= input ("Last Name:")
status= input ("Application Status(Accepted, Rejected, Pending):").capitalize()

a= "Accepted"
p= "Pending"
r= "Rejected"

accepted="""150 E 10th St. 
Claremont, CA 91775

December 2017

Dear {},

Congratulations! You have qualified and been selected to be part of this summer’s Future Rockstars Band Camp. We look forward to personally welcoming you at the orientation scheduled on June 12, 2018 from 8:00 AM to 10:00 AM. You and your guardian will be receiving all the help and information you need to ensure a smooth, comfortable transition into band camp life. 

We would like to remind you to make sure you bring the following when you arrive at camp to avoid any problems with the registration process:
	1) Your Instrument
	2) Your Papers
	3) Your self


Once again, Congratulations! We look forward to meeting you. 



Sincerely yours, 


Steven Tyler
BandCamp Master"""


pending= """150 E 10th St. 
Claremont, CA 91775

December 2017

Dear {},

Your application to FuRS has been carefully considered, and while you have met the criteria to be a future rockstar, the camp grounds has a strict threshold for how many people can be accommodated at a given time. The current period you have chosen to apply for has been filled to capacity, and therefore cannot accept any additional candidates.
While we here at Future Rockstars try our best to accommodate all qualifying individuals, this simply cannot be done. On the bright side, this is an annual summer camp, and it’s never too late to keep on rockin’!
 We encourage you to apply once again for a different time, as there are three different modules during the summer (June, July, and August) and make sure to do this early for a better chance to secure a spot. Thank you for considering FuRS, and we look forward to hearing from you again!

Sincerely yours, 


Steven Tyler
BandCamp Master"""

rejected= """150 E 10th St. 
Claremont, CA 91775

December 2017

Dear {},
We regret to inform you that your application to the Future Rockstars (FuRS) band camp has been denied for one or more reasons, but this does not mean that your journey to being a future Rockstar is over. While we cannot accommodate you at this time, there is always next year! If this does not interest you, there are many other Rockstar camps that may be more suitable for you and your needs. 
We at FuRS would never discourage you to keep working toward your goal, and perhaps explore other avenues to reach it. We always advocate for people like you to keep working hard to reach your goals, and most importantly, we would like to remind you: Don’t give up on your dreams!

Sincerely yours, 


Steven Tyler
BandCamp Master"""



accepted_output= accepted.format(firstName, lastName)
pending_output= pending.format(firstName, lastName)
rejected_output=rejected.format(firstName, lastName)

if status==a:
    print(accepted_output)
if status==r:
    print(rejected_output)
if status==p:
    print(pending_output)
