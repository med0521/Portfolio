#Python Project: Politics Daily
# Assumptions and Outline of the Game Rules
###############################################################################
# The game begins when the user selects a state. When a state is created,     #
# the game Engine will autopopulate that state with a distribution of voters  #
# determined by the outcome of the 2020 General Election. Every state has     #
# 100 voters. The voters are initialized with a andomized interest in         #
# 4 policy areas: Environmental, Social, Economic, and Military.              #
# The interest is set on a 0-9 scale (low-high). Republicans                  #
# are initialized with a randomized 0-4 interest in Environmental and Social  #
# and 5-9 interest in Economic and Military issues. Democrats are initialized #
# with a randomized 5-9 interest in Social and Environmental issues, and 0-4  #
# interest in Military and Economy. This is a oversimplified representation   #
# of policy interest meant to represent the spectrum of voters in both        #
# parties. Independent voters are initialized with a randomized 4-5 interest  #
# in all policy areas.                                                        #
###############################################################################

import random
import textwrap
#data = {state:{dem:X,rep:Y,ind:Z}}
data = {'AL':{'d':37,'r':63,'i':0},'AK':{'d':43,'r':53,'i':4},'AZ':{'d':49,'r':49,'i':2},'AR':{'d':35,'r':63,'i':2},
        'CA':{'d':64,'r':35,'i':1},'CO':{'d':56,'r':42,'i':2},'CT':{'d':60,'r':40,'i':0},'DE':{'d':59,'r':40,'i':1},
        'FL':{'d':48,'r':52,'i':0},'GA':{'d':50,'r':50,'i':0},'HI':{'d':64,'r':35,'i':1},'ID':{'d':33,'r':64,'i':1},
        'IL':{'d':58,'r':41,'i':1},'IN':{'d':41,'r':57,'i':2},'IA':{'d':45,'r':53,'i':2},'KS':{'d':42,'r':56,'i':2},
        'KY':{'d':36,'r':62,'i':2},'LA':{'d':40,'r':59,'i':1},'ME':{'d':53,'r':44,'i':3},'MD':{'d':66,'r':33,'i':1},
        'MA':{'d':66,'r':33,'i':1},'MI':{'d':51,'r':48,'i':1},'MN':{'d':46,'r':53,'i':1},'MS':{'d':41,'r':58,'i':1},
        'MO':{'d':42,'r':57,'i':1},'MT':{'d':41,'r':57,'i':2},'NE':{'d':40,'r':59,'i':1},'NV':{'d':50,'r':48,'i':2},
        'NH':{'d':53,'r':46,'i':1},'NJ':{'d':58,'r':42,'i':0},'NM':{'d':55,'r':44,'i':1},'NY':{'d':61,'r':38,'i':1},
        'NC':{'d':49,'r':50,'i':1},'ND':{'d':32,'r':66,'i':2},'OH':{'d':46,'r':54,'i':0},'OK':{'d':33,'r':66,'i':1},
        'OR':{'d':41,'r':57,'i':2},'PA':{'d':50,'r':49,'i':1},'RI':{'d':60,'r':49,'i':1},'SC':{'d':44,'r':55,'i':1},
        'SD':{'d':36,'r':62,'i':2},'TN':{'d':38,'r':61,'i':1},'TX':{'d':47,'r':52,'i':1},'UT':{'d':38,'r':59,'i':1},
        'VT':{'d':67,'r':31,'i':2},'VA':{'d':55,'r':44,'i':1},'WA':{'d':59,'r':39,'i':2},'DC':{'d':93,'r':6,'i':1},
        'WV':{'d':30,'r':69,'i':1},'WI':{'d':50,'r':49,'i':1},'WY':{'d':27,'r':71,'i':2}}

#State Class
class State:
    """Representation of a US State.
    Attributes:
    name
    rep_start
    dem_start
    ind_start
    rep_voters
    dem_voters
    events
    politicians
    elected_official
    voters

    Methods:
    vote()
    """
    #pull data and assign start distribution of voters by party
    def __init__(self,name,d,r,i):
        self.name = name
        self.rep_start = r
        self.dem_start = d
        self.ind_start = i
        self.rep_voters = 0
        self.dem_voters = 0
        self.events = []
        self.politicians = []
        self.elected_official = ''
        self.voters = []
    #Function to calculate the votes of each voter object in the state parent class
    def vote(self):
        """Calculates the interest of a user and casts a corresponding vote. Elects a politician."""
        for voter in self.voters:
            #voting is influenced by the party the person started in
            if voter.party_start == 'd':
                #if dem voter has an extremely high interest in a republican policy area, vote rep
                if voter.economic_interest >= 7 or voter.military_interest >= 7:
                    if voter.environmental_interest < 7 and voter.social_interest < 7:
                        voter.party_vote = 'r'
                    else:
                        continue
                #if dem voter has moderate interest in both rep policy areas and low in dem, vote rep
                elif 5 >= voter.economic_interest <= 6 and 5 <= voter.military_interest <= 6:
                    if voter.environmental_interest <= 2 or voter.social_interest <= 2:
                        voter.party_vote = 'r'
                else:
                    voter.party_vote = 'd'
            elif voter.party_start == 'r':
                #if rep voter has extremely high interest in democratic policy area, vote dem
                if voter.environmental_interest >= 7 or voter.social_interest >= 7:
                    if voter.military_interest < 7 and voter.economic_interest < 7:
                        voter.party_vote = 'd'
                #if rep voter has moderate interest in both dem policy areas and low in rep, vote dem
                elif 5 >= voter.environmental_interest <= 6 and 5 <= voter.social_interest <= 6:
                    if voter.military_interest <= 2 or voter.economic_interest <= 2:
                        voter.party_vote = 'd'
                    else:
                        voter.party_vote = 'r'
                else:
                    voter.party_vote = 'r'
            else:
                #handle independent voters by weighting their interests
                if voter.environmental_interest >= 5 and voter.social_interest >= 5:
                    if voter.military_interest < 5 or voter.economic_interest < 5:
                        voter.party_vote = 'd'
                elif voter.military_interest >= 5 and voter.economic_interest >= 5:
                    if voter.environmental_interest < 5 or voter.social_interest < 5:
                        voter.party_vote = 'r'
                else:
                    #if any voters are evenly interested in rep & dem policy areas
                    recent = self.events[-1]
                    #vote according to the most recently broadcast event
                    if recent.policy_area == 'environmental_interest':
                        voter.party_vote = 'd'
                    elif recent.policy_area == 'social_interest':
                        voter.party_vote = 'd'
                    elif recent.policy_area == 'military_interest':
                        voter.party_vote = 'r'
                    elif recent.policy_area == 'economic_interest':
                        voter.policy_area = 'r'
                    else:
                        raise Exception('No events have been played.')
        #count the votes for republican and democratic parties
        for voter in self.voters:
            if voter.party_vote == 'r':
                self.rep_voters += 1
            else:
                self.dem_voters += 1
        #assign the votes to a corresponding party politician in the state
        for politician in self.politicians:
            if politician.political_party == 'Republican':
                politician.votes = self.rep_voters
            else:
                politician.votes = self.dem_voters
        #determine which politician wins, according to the amount of votes cast for each party
        if self.dem_voters > self.rep_voters:
            self.elected_official = [pol for pol in self.politicians if pol.political_party == 'Democratic']
        elif self.rep_voters > self.dem_voters:
            self.elected_official = [pol for pol in self.politicians if pol.political_party == 'Republican']
        else:
            self.elected_official = ['Tie']


#Politician Class
class Politician(State):
    """Representation of a figurative state politician who belongs to either
    the Democratic or Republican Parties. There are two Politicians in every
    State.
    Attributes:
    state
    political_party
    votes
    """

    def __init__(self,state,political_party,votes = 0):
        self.state = state
        self.political_party = political_party
        self.votes = votes

#News Outlet Class
class News_Outlet(State):
    """Representation of a news outlet. Each State has one generic news outlet,
    which all voters theoretically watch.
    Attributes:
    state
    """

    def __init__(self,State):
        self.state = State

    def broadcast_event(self,state,event_to_broadcast):
        """Takes in an event and state, increases policy interest, and tracks event"""
        for voter in self.state.voters:
            voter.increase_interest(event_to_broadcast.policy_area)
        state.events.append(event_to_broadcast)

#Voter Class
class Voter(State):
    """Representation of a Voter in a State. There are 100 voters assigned to
    every State.
    Attributes:
    state
    party_start
    party_vote

    Methods:
    increase_interest()
    """

    def __init__(self,state,party_start):
        self.state = state
        self.party_start = party_start
        self.party_vote = ''
        #sets a randomized interest on a scale 0-9 by party line policy areas
        # 0-4 interest if party policy area, 5-9 interest if not
        if self.party_start == 'r':
            self.environmental_interest = random.randint(0,4)
            self.social_interest = random.randint(0,4)
            self.military_interest = random.randint(5,9)
            self.economic_interest = random.randint(5,9)
        elif self.party_start == 'd':
            self.environmental_interest = random.randint(5,9)
            self.social_interest = random.randint(5,9)
            self.military_interest = random.randint(0,4)
            self.economic_interest = random.randint(0,4)
        else:
            #for independents, randomize neutral interest in all policy areas
            self.environmental_interest = random.randint(4,5)
            self.social_interest = random.randint(4,5)
            self.military_interest = random.randint(4,5)
            self.economic_interest = random.randint(4,5)

    def increase_interest(self, policy_area):
        """Takes in a policy area, increases corresponding voter interest.
        Voter interest cannot be greater than 9."""
        if policy_area == 'environmental_interest' and self.environmental_interest < 9:
            self.environmental_interest += 1
        elif policy_area == 'social_interest' and self.social_interest < 9:
            self.social_interest += 1
        elif policy_area == 'military_interest' and self.military_interest < 9:
            self.military_interest += 1
        elif policy_area == 'economic_interest' and self.economic_interest < 9:
            self.economic_interest += 1
        else:
            pass

#Events Class
class Event:
    """Representation of an event occuring in a generalized category of events,
    meant to correlate to common public policy interest areas.
    Attributes:
    name
    policy_area
    """

    def __init__(self, name, policy_area):
        self.name = name
        self.policy_area = policy_area

#Engine Class
class Engine:
    """
    Play as a state's News Outlet by entering simulated events in the game.
    Event options are listed in the Event Menu. Enter 'election' to end the game.
    Attributes:
    events_menu
    states_menu
    events_played
    election_results
    user_state

    Methods:
    play()
    send_event()
    printer()
    """

    events_menu = {'E':{'name':'Environmental Disaster','policy':'environmental_interest'},
                   'F':{'name':'Financial Downturn','policy':'economic_interest'},
                   'U':{'name':'Unemployment Spike','policy':'economic_interest'},
                   'H':{'name':'Health Pandemic','policy':'social_interest'},
                   'W':{'name':'US Enters Foreign War','policy':'military_interest'},
                   'D':{'name':'Domestic Terrorist','policy':'military_interest'},
                   'S':{'name':'Social Justice March','policy':'social_interest'}}

    states_menu = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS',
                   'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY',
                   'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'DC',
                   'WV', 'WI', 'WY']

    def __init__(self):
        self.events_played = []
        self.election_results = {}
        self.user_state = 0

    def play(self):
        """Controls game flow and prompts user for inputs. Handles printing to the user's terminal."""
        #print instructions to the user, then print the state obbreviation options
        self.printer('startgame')
        self.printer('statemenu')
        #get the state from the user to initiate the game
        state = input('To start the game, enter a State from the abbreviations menu: ').upper()
        print(' ')
        #handle input errors for states
        while state not in self.states_menu:
            if state == 'HELP':
                print(self.__doc__)
                state = input('To start the game, enter a State from the abbreviations menu: ').upper()
                if state in self.states_menu:
                    break
            state = input('Please enter a valid State abbreviation: ').upper()
        #create a State object and populate with voter data from dataset
        self.user_state = State(state,data[state]['d'],data[state]['r'],data[state]['i'])
        #create voter objects according to state party distribution
        for i in range(data[state]['d']):
            self.user_state.voters.append(Voter(state,'d'))
            i+=1
        for i in range(data[state]['r']):
            self.user_state.voters.append(Voter(state,'r'))
            i+=1
        for i in range(data[state]['i']):
            self.user_state.voters.append(Voter(state,'i'))
            i+=1
        #create politician objects for each party in the state
        self.user_state.politicians.append(Politician(state,'Republican'))
        self.user_state.politicians.append(Politician(state,'Democratic'))
        #create the news outlet object for the state
        news = News_Outlet(self.user_state)
        #print event options to the user and instructions for how to input
        self.printer('eventsmenu')
        print('')
        print('Enter the event abbreviation when prompted ("E",etc.)')
        print('')

        current = ''
        #prompt the user for events to broadcast to voters in the simulated state
        while current != 'ELECTION':
            current = input('Enter a news story to broadcast to voters in {}.'.format(state)).upper()
            #help screen
            if current == 'HELP':
                print(self.__doc__)
                continue
            if current != 'ELECTION' and current in self.events_menu.keys():
                #create event object based on user input
                event_to_send = Event(self.events_menu[current]['name'],self.events_menu[current]['policy'])
                #send event to the news object, which then broadcasts to viewers
                self.send_event(news,self.user_state,event_to_send)
            elif current != 'ELECTION' and current not in self.events_menu.keys():
                print('Please enter a valid event from the menu.')
            print(' ')
        #if election is called, intiate the vote method and cast election results
        if current == 'ELECTION':
            self.user_state.vote()
            self.election_results['elected'] = self.user_state.elected_official
            #print results to the user
            self.printer('results')

    def send_event(self,news_outlet,state,event_to_send):
        """Sends event objects to the News object. Takes a news and event object as inputs."""
        self.events_played.append(event_to_send)
        news_outlet.broadcast_event(state,event_to_send)

    def printer(self,option):
        """Takes an option input and prints to the user a corresponding formatted output."""
        if option == 'startgame':
            print(" ")
            print("Welcome to Politics Daily!")
            print(" ")
            print("Politics is a funny game. To win at politics, a politician\nneeds to be in the right place at the right time.")
            print("Catching the right news cycles and voter interest give you an edge.")
            print("How much can the news sway voter attention? Let's find out.")
            print(" ")
            print("To begin, select a state. Your state's voters only watch one news channel,\nand you call the shots on what stories get broadcast.")
            print("Play out different scenarios, and see how simulated events influence voters.")
            print("When the election is called, all votes are cast and a politician is elected.")
            print(" ")
        elif option == 'statemenu':
            printed = """
                            +----------------------------------------------------------------------+
                            | State Abbreviation Menu:                                             |
                            | AL Alabama     HI Hawaii    MA Mass.      NM New Mexico VA Virginia  |
                            | AK Arkansas    ID Idaho     MI Michigan   NY New York   WA Wash.     |
                            | AZ Arizona     IL Illinois  MN Minnesota  NC N Carolina DC Wash D.C. |
                            | AR Arkansas    IN Indiana   MS Miss.      NC N Dakota   WV W Virginia|
                            | CA California  IA Iowa      MO Missouri   SC S Carolina WI Wisconsin |
                            | CO Colorado    KS Kansas    MT Montana    SD S Dakota   WY Wyoming   |
                            | CT Connecticut KY Kentucky  NE Nebraska   TN Tenn.                   |
                            | DE Delaware    LA Louisiana NV Nevada     TX Texas                   |
                            | FL Florida     ME Maine     NH New Hamp.  UT Utah                    |
                            | GA Georgia     MD Maryland  NJ New Jersey VT Vermont                 |
                            +----------------------------------------------------------------------+"""
            print(textwrap.dedent(printed))
        elif option == 'eventsmenu':
            printed = """
                            +-------------------------------------------+
                            | Event Menu:                               |
                            |  E: Environmental Disaster                |
                            |  F: Financial Downturn                    |
                            |  U: Unemployment Spike                    |
                            |  H: Health Pandemic                       |
                            |  W: US Enters Foreign War                 |
                            |  D: Domestic Terrorist                    |
                            |  S: Social Justice March                  |
                            |(enter 'election' to initiate the election)|
                            |(enter 'help' for help)                    |
                            +-------------------------------------------+"""
            print(textwrap.dedent(printed))
        elif option == 'results':
            #print to the user their starting information
            print('Simulated Election Results:')
            print('-'*50)
            print("Selected State: {}".format(self.user_state.name))
            print("Starting Voter Distribution: {}% Rep {}% Dem {}% Ind".format(self.user_state.rep_start,self.user_state.dem_start,self.user_state.ind_start))
            print("Events Played:")
            #print to the user a summary of events they broadcast to their voters
            for event in self.events_played:
                print(event.name,end='\n')
            print("Election Results: {}% Rep {}% Dem".format(self.user_state.rep_voters,self.user_state.dem_voters))
            if self.user_state.elected_official == ['Tie']:
                print('Tie!')
            else:
                #print the change in party votes from the starting distribution if there is a winner
                if self.user_state.rep_start > self.user_state.rep_voters:
                    print("% Republican change: -{}%".format(self.user_state.rep_start - self.user_state.rep_voters))
                elif self.user_state.rep_start < self.user_state.rep_voters:
                    print("% Republican change: +{}%".format(self.user_state.rep_voters - self.user_state.rep_start))
                else:
                    print("% Republican change: None")
                if self.user_state.dem_start > self.user_state.dem_voters:
                    print("% Democratic change: -{}%".format(self.user_state.dem_start - self.user_state.dem_voters))
                elif self.user_state.dem_start < self.user_state.dem_voters:
                    print("% Democratic change: +{}%".format(self.user_state.dem_voters - self.user_state.dem_start))
                else:
                    print("% Democratic change: None")
                print("Winner: {} Candidate".format(self.user_state.elected_official[0].political_party))

        else:
            pass


## Game begins by creating a game engine object and calling the play method
game = Engine()
game.play()
