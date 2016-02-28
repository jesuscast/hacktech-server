BioPass
=======
Login into any website using only your fingeprint. Biometrics are not a field of only the goverment and academics anymore. In recent years, advancements of technology have enable mass use of powerful sensors such as synaptics fingerprint sensor. Now we need to exploit this power by creating the next generation of services. Our product's security relies in industry standard encryption algorithms and best practices. Our fingerprint matching technology is built on top of open source code developed by the United States Goverments Federal Agency. Although we do not own the intellectual property of many of those algorithms - since they are widely academically known -, our integration with advanced web technologies can lead a potential standard..

Inspiration
=======
Jesus Castaneda always wanted to use fingerprint sensors. During a hackathon at Pasadena some sensors were available and this project was born. Although this project was done in a rush we hope to improve the security of the system, by streaming the data directly from the device to the network without physical storage in between, by using better encryption techniques, and by providing an API for websites to integrate (instead of our current hijacking methods).

Mechanism
=======
The system consists of three components.
1) A Google Chrome extension.
2) A Python daemon on the client.
3) A Web Server with matching technology.

The Google Chrome extension:
It lies on the client's browser looking for possible login opportunities by looking at the HTML.
If such a login opportunity exists it compares the current domain against a database to see if there is information already saved for this website. There are two possible possibilities now:
1) There is no information saved: This leads to a checkbox next to the login form that indicates whether you desire to store those credentials for use with your fingerprint.
2) There is information saved: In this case the extension would communicate this to the server and wait for a fingeprint signal sent from the server.

The Sever:
The server consists of a couple python scripts that glue together several components:
1) First it listens for upcoming connections.
2) It cleans up raw fingerprints received.
3) Then it applies transformations to the bmp file in order to obtain the feature rich file used by the matching algorithm
4) It feeds the processed images to a c library for matching.
5) Keeps track of users, credentials, and domains.

Python daemon:
It lies in the client machine listening for images outputted from the fingerprint sensor into the filesystem.
Once a new image appears it sends it over the network (TODO: encrypt it before sendind)
