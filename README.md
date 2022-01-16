# StatsCan-Citer
Automatically create citations based on StatsCan data.


Here is the python script, as well as the application, which automatically generates the citation that must be placed in a bibliography.
The application was built with tkinter, and generated with pyinstaller.
The data is obtained with BeautifulSoup, to fetch the catalogue no., relevant date, and title information.
Statistic's Canada use unique catalogue no.s to distinguish between their datatables.
Klembord stylizes the text (as citations often need italics) which is then copied to clipboard with Pyperclip.

*IMPORTANT* User must enter url of a particular 'type'. See FUNCTIONALITY below.

This application is no-nonsense. It will not handle a user's misbehaving.
The structure of the citations isn't guaranteed to conform with the respective body's citation guide.
Unfortunately, there is no clear citation example (in any of the 4 provided) which captures an institution equivalent to Statistic's Canada.
For this reason I advise *caution.*
If anyone (particularly Statistic's Canada, or any of the respective bodies) could point to references or examples on how to better format the citation, I will update the file.
An individual could also just copy the code and update the string themselves, they are located at lines:
MLA: 200
APA: 245
Chicago: 290
IEEE: 335

Klembord was a bit cumbersome, and still technically throws errors, however, it doesn't affect functionality.
It would be nice to have a button which generates the strings with one click, without having to request the website each time a button is clicked.
The latter was done because klembord misbehaved for me when trying to store things globally, to access afterwards.

I would like to update the UI and make it visually pleasant.

FUNCTIONALITY:
Here are some examples of how the code works, with the following URL:
https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/dt-td/Rp-eng.cfm?LANG=E&APATH=3&DETAIL=0&DIM=0&FL=A&FREE=0&GC=0&GID=0&GK=0&GRP=1&PID=111822&PRID=10&PTYPE=109445&S=0&SHOWALL=0&SUB=0&Temporal=2017&THEME=123&VID=0&VNAMEE=&VNAMEF=

1: The application
![empty_app](https://user-images.githubusercontent.com/93615107/149674320-aa304b88-e40c-409b-b55a-2aeff7f0599c.png)

2: Filled with only URL
![url_only](https://user-images.githubusercontent.com/93615107/149674454-cdc97d4f-c503-46a2-b39f-e5fbcb5aac78.png)

3: Filled in all fields
![filled_app](https://user-images.githubusercontent.com/93615107/149674466-808a13af-4b9e-45b3-a745-f523d9623ba3.png)

Here's an example of what was generated by clicking the buttons at step (2: Filled with only URL)
For each of the 4 types:
![empty_citations](https://user-images.githubusercontent.com/93615107/149674659-f8c33d39-c235-4bfd-abdc-ccc233bc3c90.png)

Here's an example of what was generated by clicking the buttons at step (3: Filled in all fields)
For each of the 4 types:
![filled_citations](https://user-images.githubusercontent.com/93615107/149674675-fe99b9a7-0b12-4134-81c3-00cb76387072.png)



Check the releases on my Github for the application: statscan_citation
