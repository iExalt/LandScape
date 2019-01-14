# Improvements
## Style
- Scrolling down on the API docs page from the top to "Authentication" is jarring (Chrome 71.0.3578.98) 
i.e when the API Token/Set Token bar turns from a static element on the page to a sticky element on the top of your viewport.
- Scrolling up from when the sticky element turns back to static is even worse. Makes reading the first paragraph "Authentication" almost impossible, which is bad because it's arguably the most important paragraph of them all.
- Consider splitting the long API docs page into multiple pages.
  - Not to show any favoritism, but Hashicorp generally nails their API documentation, and the [Vault API docs](https://www.vaultproject.io/api/overview.html) are a fantastic exemplar of how a ton of API endpoints can be documented and divided into smaller, more managable & readable chunks while still being rich in information and examples for the end user.

## Technical
- I had a cool full feature test planned for LandScape where it would create a host, run commands against it to install (say) Docker/Kubernetes against it with a simple web server, curl the endpoint (and then destroy the host) to verify that everything was working correctly, but I couldn't seem to add an ssh key to any host that I'd create. Didn't quite have time to debug this so the feature was scrapped. First lines of [Gist](https://gist.github.com/iExalt/eb33ba0d9d85d7cd9a656279b51d3cc7).
- The difference between a "project" token/API key and a non-project ("global"?) token/API key isn't immediately obvious and the nuances go further than just "a project token can't affect other projects". The differences aren't clearly defined anywhere easily found in the documentation. For example, trying to curl the "/capacity" endpoint with a project token fails. Last line of [Gist](https://gist.github.com/iExalt/eb33ba0d9d85d7cd9a656279b51d3cc7). 
  - I suspect there are more "gotchas" like the above lurking around.

## Minor Considerations
- [tech_1.md](https://github.com/packethost/about-us/blob/master/tech_1.md) needs to be updated, the "/plan" endpoint shoud be "/plans"
- [This URL](https://www.packet.com/developers/api/#retrieve-a-projects-ssk-keys) has a typo; "ssk-keys" -> "ssh-keys"


## Thoughts
- Overall, I definitely enjoyed this experience! I haven't made many "customer/end-user" facing python tools (most of what I've made has been developer/internal-facing i.e just enough of an interface to get the job done), so the nuances of making a proper CLI, something that's worthy of say... *docker* or *python3-openstackclient* was an interesting challenge for me. A lot more time was spent trying to wrangle *argparse* than say, debugging REST requests - but that's good! It means that I actually learned something, and I'm not just going through the motions.
  - The challenge felt relevant to my previous experience, what Packet does, and what a SE intern might actually do in the real world.
- I took the liberty of peeking through coding_fun.md and looking at some of the WIP challenges. Being a customer seems most in line with the current challenge in place, and also gives something of a concrete goal to work towards. Good stuff.
