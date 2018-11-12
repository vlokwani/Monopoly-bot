import random as rand
import copy


class State(object):
    """ State object to be maintained """
    def __init__(self):
        self.state = {
            turn: 0,
            current_player: 0,
            jailed: [False, False],
            status: [0] * 30,
            position: [0,0],
            liquid_cash: [0,0],    #Cash in hand,
            total_wealth: [0,0],   #Cash + Buildings + Face value of property,
            liquid_assets:[0,0],   #Cash + Face value of prop,
            phase: None,           #Phase when the game begins, this will be changed later, 
            phase_info: None,
            debt: 0,
            previous_states: [],
            card_history:],
            percent_own_buildings:0.0, 0.0], #[addons_p1, addons_p2],
            percent_own_money:[0, 0],
            total_transacted_wealth: [0.0, 0.0],
            trades_p1: [],         #[([properties], price, accepted)],
            trades_p2: [],         #[([properties], price, accepted)],
            trades_attepmted:0, 0],
            hotels_left: 12,
            houses_left: 32,
            monopolies_held: [0] * 10,
            p1_net_wealth: 0,
            p2_net_wealth: 0,
        }
        

    def generate_state(self, *args, **kwargs):
        """ 
            generate a state with random plausible values.
            Ideally this function will have to be called before every test case is executed.
        """
        state, new_state = copy.deepcopy(self.state), copy.deepcopy(self.state)
        # stub for transforming the state according to our needs
        return state, new_state


class TestAdjudicator(object): 
    """ 
    Contains all test cases that will be run for different calls 
    of the Adjudicator.
    """
    def __init__(self, ajudicator, agent1, agent2):
        self.adjudicator = adjudicator
        self.p1 = agent1
        self.p2 = agent2
        self.state = State()


    # Buy property routines
    

    # Auction routines 


    # Jail Routines


    # Pay Rent routines


    # Building houses and hotel routines


    # Selling hourses and hotel routines


    # Mortgage routines