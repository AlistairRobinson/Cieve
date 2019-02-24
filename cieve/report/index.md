---


---

<h1 id="cieve-final-report">Cieve Final Report</h1>
<h2 id="security-and-compliance">Security and Compliance</h2>
<p>Cyber security is the process of securing and protecting digital systems from exploitation. Our team decided that security should be a consideration throughout all stages of development for our software engineering project to ensure that the final product would not be vulnerable to attacks from malicious parties.</p>
<p>Additionally, with the recent introduction of stricter data protection laws through the EU’s GDPR, the team also decided to ensure that the final product would be fully GDPR compliant by carefully controlling stored and processed data and obtaining user consent.</p>
<h3 id="vulnerability-protection">Vulnerability Protection</h3>
<p>The OWASP Top Ten, a consensus of the ten most critical web application security vulnerabilities, was used as a guide for vulnerabilities that the application should be protected against. (<a href="https://www.owasp.org/images/7/72/OWASP_Top_10-2017_%28en%29.pdf.pdf">https://www.owasp.org/images/7/72/OWASP_Top_10-2017_(en).pdf.pdf</a>)</p>
<p>The risk of a SQL injection attack was mitigated through the use a NoSQL database, MongoDB. NoSQL databases are fully protected against SQL injection. Unit tests were also included to verify protection against NoSQL injection, a similar attack.</p>
<p>The risk of a XSS attack was mitigated through our choice of web server framework. Python Flask automatically sanitises user input and server output to protect against these attacks. (<a href="http://flask.pocoo.org/docs/1.0/security/">http://flask.pocoo.org/docs/1.0/security/</a>)</p>
<p>The risk of a CSRF attack was mitigated through the use of CSRF tokens. These unique CSRF tokens are generated when a page is loaded added to a user’s session. When the user posts data to the server, they attach the CSRF token unique to their session. The server checks that these two tokens are equivalent and blocks requests it identifies as suspicious.</p>
<p>The risk of an authentication breach was mitigated through the use of a non-enumerated ID system to generate session variables. This means it would be harder for an attacker to guess another user’s user ID to impersonate them through session variable manipulation. Authentication checks were also checked using unit tests. PBKDF2, a secure, industry standard hashing algorithm was used to hash salted user passwords. <strong>Complexity checks were also used to ensure that users only used secure passwords of a certain length and complexity</strong>.</p>
<h3 id="data-protection-compliance">Data Protection Compliance</h3>
<h3 id="dependency-security">Dependency Security</h3>
<p>It is not only necessary for our system to be secured against attacks, but also the frameworks and tools used inside the project. We read security documentation for each technology used to verify that they did not add an additional risk to our system. We have listed this security documentation for your verification:</p>
<ul>
<li>Python Flask (<a href="http://flask.pocoo.org/docs/1.0/security/">http://flask.pocoo.org/docs/1.0/security/</a>)</li>
<li>MongoDB Atlas (<a href="https://docs.mongodb.com/manual/security/">https://docs.mongodb.com/manual/security/</a>) (<a href="https://www.mongodb.com/cloud/atlas/faq#compliance">https://www.mongodb.com/cloud/atlas/faq#compliance</a>) (<a href="https://www.mongodb.com/cloud/trust">https://www.mongodb.com/cloud/trust</a>) (<a href="https://docs.mongodb.com/manual/security/">https://docs.mongodb.com/manual/security/</a>)</li>
<li>GitHub (<a href="https://github.com/security">https://github.com/security</a>)</li>
<li>Travis CI (<a href="https://docs.travis-ci.com/legal/security">https://docs.travis-ci.com/legal/security</a>)</li>
</ul>
<h2 id="test-driven-development">Test Driven Development</h2>
<p>Following Deutsche Bank’s guest lecture on how they utilise test driven development in their technology divisions, it was decided by consensus that one team member would be responsible for building unit tests to ensure that functionality was correctly implemented. Furthermore, this allowed us to perform quantitative success measurement near the end of the development process.</p>
<h3 id="build-verification">Build Verification</h3>
<p>When using parallel version control through the use of different branches in Git, it became difficult for us to verify the integrity of our branches before merging with master. Therefore, we utilised a Continuous Integration (CI) platform, Travis CI (<a href="https://travis-ci.com/">https://travis-ci.com/</a>), to verify each concurrent version of code throughout the development cycle. Travis runs pushed code, taken from each available branch, in a virtual machine to ensure that it works correctly. If a build passes, the push is verified. We integrated this CI tool into our <code>README.md</code> file to make it easy for all team members to see the progress of their builds.</p>
<p><img src="https://i.imgur.com/sGuoUJ6.png" alt="Cieve build verification"></p>
<p>The use of a CI tool assisted all sub-teams in identifying issues with their code which had unintended consequences.</p>
<h3 id="unit-testing">Unit Testing</h3>
<p>As stated in our initial documents, Pytest was decided as the</p>
<h3 id="user-testing">User Testing</h3>
<h3 id="success-measurement">Success Measurement</h3>
<h2 id="project-management">Project Management</h2>
<h3 id="team-structure">Team Structure</h3>
<p>It was decided early on that our software engineering team should specialise into different areas whilst utilising pair programming techniques to ensure that each aspect of the deliverable was fully understood by at least two team members. With this in mind, we separated into three sub-teams with each team member being assigned individual responsibilities:</p>

<table>
<thead>
<tr>
<th>Name</th>
<th>Sub-team</th>
<th>Title</th>
<th>Technologies Used</th>
<th>Responsibility</th>
</tr>
</thead>
<tbody>
<tr>
<td>Josh Hankins</td>
<td>Frontend</td>
<td>Lead Designer</td>
<td>HTML/CSS, Bulma</td>
<td>Using the Bulma frontend framework, develop an adaptive, intelligent user interface compatible across multiple devices</td>
</tr>
<tr>
<td>Abdullah Khan</td>
<td>Frontend</td>
<td>Business Analyst</td>
<td>JavaScript</td>
<td>Using Asynchronous JavaScript (AJAX) client side functionality, provide users with a seamless interface between the frontend and backend systems. Act as the primary contact for communications between the development team and the client</td>
</tr>
<tr>
<td>Nathan Hall</td>
<td>Backend</td>
<td>Project Manager</td>
<td>Python, Flask</td>
<td>Using the Python Flask web server framework, develop the web server to provide the main functionality of the product. Lead the management of the team, arranging meetings and acting as scrum master</td>
</tr>
<tr>
<td>Alistair Robinson</td>
<td>Backend</td>
<td>Security, Testing and Compliance Officer</td>
<td>Python, Pytest</td>
<td>Using the Pytest unit testing framework, maintain software tests to mitigate security risks, perform success measurement and verify data protection compliance. Oversee usage of version control and fix merge conflicts</td>
</tr>
<tr>
<td>Felix Gaul</td>
<td>Data</td>
<td>Database Controller</td>
<td>Python, MongoDB Atlas</td>
<td>Using MongoDB’s scalable cloud database platform, Atlas, develop a logical database schema and a database access class in the Python backend to store user data</td>
</tr>
<tr>
<td>Justas Tamulis</td>
<td>Data</td>
<td>Machine Learning Developer</td>
<td>Python, MongoDB Atlas</td>
<td>Using machine learning techniques in Python, develop an intelligent way of ranking applicants such that applicants are prioritised for relevant roles intelligently.</td>
</tr>
</tbody>
</table><p>By splitting our workload as such, we were able to strike a balance between specialisation through division of labour and information sharing through pair programming. Having designated sub-teams encouraged focused teamwork between team members, for example, when implementing AJAX requests between the frontend and the backend systems.</p>
<h3 id="development-approach">Development Approach</h3>
<p>As outlined in our design and requirements documents, it was decided that our team should follow the Scrum agile development methodology to allow us to quickly adapt to changes in our requirements in our relatively short development time of 9 weeks. Our sprints cycles (from Week 5 to Week 9) had a length of 3-4 days, allowing for two sprint cycles per week. This period was longer than most sprint cycles used in industry, however, a longer period allowed team members to more effectively balance external commitments and reflected the fact that we were not working on the project in the same environment full time. Each sub-team assigned a goal for each sprint as such:</p>

<table>
<thead>
<tr>
<th>Sprint Number</th>
<th>Date Started</th>
<th>Date Completed</th>
<th>Frontend Target</th>
<th>Backend Target</th>
<th>Data Target</th>
</tr>
</thead>
<tbody>
<tr>
<td>Sprint 1</td>
<td>08/02/2019</td>
<td>12/02/2019</td>
<td>Translate frontend mock up to Flask templates</td>
<td>Implement authentication framework</td>
<td>Identify required database access and modification functions</td>
</tr>
<tr>
<td>Sprint 2</td>
<td>12/02/2019</td>
<td>15/02/2019</td>
<td>Translate frontend mock up to Flask templates</td>
<td>Start basic job creation framework</td>
<td>Complete database access and modification functions</td>
</tr>
<tr>
<td>Sprint 3</td>
<td>15/02/2019</td>
<td>19/02/2019</td>
<td>Add basic JavaScript to completed templates</td>
<td>Fix unit testing framework</td>
<td>Complete database access and modification functions</td>
</tr>
<tr>
<td>Sprint 4</td>
<td>19/02/2019</td>
<td>22/02/2019</td>
<td>Add AJAX requests to completed templates</td>
<td>Implement job creation framework</td>
<td>Implement machine learning feedback functions</td>
</tr>
<tr>
<td>Sprint 5</td>
<td>22/02/2019</td>
<td>25/02/2019</td>
<td>Fix page routing</td>
<td>Implement job search functionality</td>
<td>Finalise machine learning design</td>
</tr>
</tbody>
</table><p>Team meetings were scheduled to be once a week (Friday) during the outline planning phase, then twice a week (Tuesday and Friday) after the beginning of development to reflect the length of our sprint cycles. Meetings were scheduled in a causal but focused environment to maximise productivity and minutes of each meeting were taken to ensure that absent team members did not fall behind.</p>
<h3 id="version-control">Version Control</h3>
<p>To allow for concurrent development between development teams, we utilised Git version control software. Git allows software to be developed in parallel through the use of branches, which can be developed independently and merged periodically to allow different team members to work on different sections of the project. We used a cloud based Git hosting platform, GitHub, to allow remote access to our Git repository. <strong>The use of GitHub also allowed us to use Travis to perform build verification, discussed in the testing section</strong>.</p>
<p>Three development branches were created to allow each sub-team to work on their sprint cycles without affecting the work of other team members. The frontend team were restricted to committing to the <code>frontend</code> branch, and so on. At the end of each sprint cycle, it was Alistair’s responsibility to merge the three branches together into <code>master</code> to synchronise the shared versions of code and to resolve any resulting merge conflicts. However, we did not merge if any sub-team was not confident in the correctness or completeness of their committed code to preserve the integrity of the master branch.</p>
<pre><code>- master
| - frontend
| - backend
| - data
</code></pre>
<p>Version control was challenging during our development cycle since only two members of our team were familiar with using the Git version control software. This meant that all other team members had to familiarise themselves with Git, which led to a small number of merge conflicts early in development. However, after team members invested more time into learning and using Git, we found that the frequency of merge conflicts decreased and our development process became more streamlined.</p>

