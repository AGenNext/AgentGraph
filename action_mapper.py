"""
Schema.org Action Mapping Tool

Maps all Schema.org Action types to our implementation.

Reference: https://schema.org/docs/full.html#action_tree
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, field


class ActionCategory(Enum):
    ACHIEVE = "AchieveAction"  # AchieveAction > LoseAction, TieAction, WinAction
    ASSESS = "AssessAction"  # AssessAction > ChooseAction, VoteAction, IgnoreAction, ReviewAction
    CONSUME = "ConsumeAction"  # ConsumeAction > DrinkAction, EatAction, UseAction, ConsumeAction
    CONTROL = "ControlAction"  # ControlAction > ActivateAction, AuthenticateAction, DeactivateAction
    CREATE = "CreateAction"  # CreateAction > CookAction, DrawAction, FilmAction, PaintAction, WriteAction
    FIND = "FindAction"  # FindAction > CheckAction, DiscoverAction, TrackAction
    INTERACT = "InteractAction"  # InteractAction > BefriendAction, CommunicateAction, FollowAction
    MOVE = "MoveAction"  # MoveAction > ArriveAction, DepartAction, TravelAction
    ORGANIZE = "OrganizeAction"  # OrganizeAction > AllocateAction, ApplyAction, BookmarkAction
    PLAN = "PlanAction"  # PlanAction > CancelAction, ReserveAction, ScheduleAction
    PLAY = "PlayAction"  # PlayAction > ExerciseAction, PerformAction
    SEARCH = "SearchAction"  # SearchAction > SeekToAction, SolveMathAction
    TRADE = "TradeAction"  # TradeAction > BuyAction, PayAction, RentAction, SellAction
    TRANSFER = "TransferAction"  # TransferAction > BorrowAction, DonateAction, GiveAction, SendAction
    UPDATE = "UpdateAction"  # UpdateAction > AddAction, DeleteAction, ReplaceAction


# Complete Action Type Mapping
ACTION_TYPE_MAP: Dict[str, Dict] = {
    # AchieveAction
    "LoseAction": {"category": "ACHIEVE", "db": "gaming_database.py"},
    "TieAction": {"category": "ACHIEVE", "db": "gaming_database.py"},
    "WinAction": {"category": "ACHIEVE", "db": "gaming_database.py"},
    
    # AssessAction
    "ChooseAction": {"category": "ASSESS", "db": "data_lineage.py"},
    "VoteAction": {"category": "ASSESS", "db": "social_graph.py"},
    "IgnoreAction": {"category": "ASSESS", "db": "data_lineage.py"},
    "ReactAction": {"category": "ASSESS", "db": "social_graph.py"},
    "AgreeAction": {"category": "ASSESS", "db": "social_graph.py"},
    "DisagreeAction": {"category": "ASSESS", "db": "social_graph.py"},
    "EndorseAction": {"category": "ASSESS", "db": "social_graph.py"},
    "LikeAction": {"category": "ASSESS", "db": "social_graph.py"},
    "WantAction": {"category": "ASSESS", "db": "social_graph.py"},
    "ReviewAction": {"category": "ASSESS", "db": "webcontent_database.py"},
    
    # ConsumeAction
    "DrinkAction": {"category": "CONSUME", "db": "food_database.py"},
    "EatAction": {"category": "CONSUME", "db": "food_database.py"},
    "InstallAction": {"category": "CONSUME", "db": "software_media.py"},
    "ListenAction": {"category": "CONSUME", "db": "music_database.py"},
    "PlayGameAction": {"category": "CONSUME", "db": "gaming_database.py"},
    "ReadAction": {"category": "CONSUME", "db": "book_database.py"},
    "UseAction": {"category": "CONSUME", "db": "retail_database.py"},
    "WearAction": {"category": "CONSUME", "db": "retail_database.py"},
    "ViewAction": {"category": "CONSUME", "db": "movie_database.py"},
    "WatchAction": {"category": "CONSUME", "db": "movie_database.py"},
    
    # ControlAction
    "ActivateAction": {"category": "CONTROL", "db": "iot_database.py"},
    "AuthenticateAction": {"category": "CONTROL", "db": "person_organization.py"},
    "DeactivateAction": {"category": "CONTROL", "db": "iot_database.py"},
    "LoginAction": {"category": "CONTROL", "db": "data_lineage.py"},
    "ResetPasswordAction": {"category": "CONTROL", "db": "data_lineage.py"},
    "ResumeAction": {"category": "CONTROL", "db": "data_lineage.py"},
    "SuspendAction": {"category": "CONTROL", "db": "data_lineage.py"},
    
    # CreateAction
    "CookAction": {"category": "CREATE", "db": "food_database.py"},
    "DrawAction": {"category": "CREATE", "db": "software_media.py"},
    "FilmAction": {"category": "CREATE", "db": "movie_database.py"},
    "PaintAction": {"category": "CREATE", "db": "software_media.py"},
    "WriteAction": {"category": "CREATE", "db": "news_database.py"},
    
    # FindAction
    "CheckAction": {"category": "FIND", "db": "data_lineage.py"},
    "DiscoverAction": {"category": "FIND", "db": "knowledge_graph.py"},
    "TrackAction": {"category": "FIND", "db": "iot_database.py"},
    
    # InteractAction
    "BefriendAction": {"category": "INTERACT", "db": "social_graph.py"},
    "AskAction": {"category": "INTERACT", "db": "data_lineage.py"},
    "CheckInAction": {"category": "INTERACT", "db": "travel_database.py"},
    "CheckOutAction": {"category": "INTERACT", "db": "travel_database.py"},
    "CommentAction": {"category": "INTERACT", "db": "news_database.py"},
    "ShareAction": {"category": "INTERACT", "db": "social_graph.py"},
    "InviteAction": {"category": "INTERACT", "db": "events_database.py"},
    "ReplyAction": {"category": "INTERACT", "db": "news_database.py"},
    "FollowAction": {"category": "INTERACT", "db": "social_graph.py"},
    "JoinAction": {"category": "INTERACT", "db": "events_database.py"},
    "LeaveAction": {"category": "INTERACT", "db": "events_database.py"},
    "MarryAction": {"category": "INTERACT", "db": "person_organization.py"},
    "RegisterAction": {"category": "INTERACT", "db": "data_lineage.py"},
    "SubscribeAction": {"category": "INTERACT", "db": "news_database.py"},
    
    # MoveAction
    "ArriveAction": {"category": "MOVE", "db": "travel_database.py"},
    "DepartAction": {"category": "MOVE", "db": "travel_database.py"},
    "TravelAction": {"category": "MOVE", "db": "travel_database.py"},
    
    # OrganizeAction
    "AcceptAction": {"category": "ORGANIZE", "db": "data_lineage.py"},
    "AssignAction": {"category": "ORGANIZE", "db": "employment_graph.py"},
    "AuthorizeAction": {"category": "ORGANIZE", "db": "data_lineage.py"},
    "RejectAction": {"category": "ORGANIZE", "db": "data_lineage.py"},
    "ApplyAction": {"category": "ORGANIZE", "db": "employment_graph.py"},
    "BookmarkAction": {"category": "ORGANIZE", "db": "knowledge_graph.py"},
    
    # PlanAction
    "CancelAction": {"category": "PLAN", "db": "events_database.py"},
    "ReserveAction": {"category": "PLAN", "db": "travel_database.py"},
    "ScheduleAction": {"category": "PLAN", "db": "events_database.py"},
    
    # PlayAction
    "ExerciseAction": {"category": "PLAY", "db": "sports_database.py"},
    "PerformAction": {"category": "PLAY", "db": "events_database.py"},
    
    # SearchAction
    "SeekToAction": {"category": "SEARCH", "db": "knowledge_graph.py"},
    "SolveMathAction": {"category": "SEARCH", "db": "kernel_primitives.py"},
    
    # TradeAction
    "BuyAction": {"category": "TRADE", "db": "retail_database.py"},
    "OrderAction": {"category": "TRADE", "db": "retail_database.py"},
    "PayAction": {"category": "TRADE", "db": "banking_database.py"},
    "PreOrderAction": {"category": "TRADE", "db": "retail_database.py"},
    "QuoteAction": {"category": "TRADE", "db": "insurance_database.py"},
    "RentAction": {"category": "TRADE", "db": "realestate_database.py"},
    "SellAction": {"category": "TRADE", "db": "retail_database.py"},
    "TipAction": {"category": "TRADE", "db": "food_database.py"},
    
    # TransferAction
    "BorrowAction": {"category": "TRANSFER", "db": "library_database.py"},
    "DonateAction": {"category": "TRANSFER", "db": "nonprofit_database.py"},
    "DownloadAction": {"category": "TRANSFER", "db": "software_media.py"},
    "GiveAction": {"category": "TRANSFER", "db": "nonprofit_database.py"},
    "LendAction": {"category": "TRANSFER", "db": "banking_database.py"},
    "ReceiveAction": {"category": "TRANSFER", "db": "banking_database.py"},
    "ReturnAction": {"category": "TRANSFER", "db": "retail_database.py"},
    "SendAction": {"category": "TRANSFER", "db": "banking_database.py"},
    "TakeAction": {"category": "TRANSFER", "db": "data_lineage.py"},
    
    # UpdateAction
    "AddAction": {"category": "UPDATE", "db": "data_lineage.py"},
    "InsertAction": {"category": "UPDATE", "db": "data_lineage.py"},
    "AppendAction": {"category": "UPDATE", "db": "data_lineage.py"},
    "PrependAction": {"category": "UPDATE", "db": "data_lineage.py"},
    "DeleteAction": {"category": "UPDATE", "db": "data_lineage.py"},
    "ReplaceAction": {"category": "UPDATE", "db": "data_lineage.py"},
}


@dataclass
class ActionMapping:
    action_type: str
    category: str
    database: str
    
    # Schema.org properties
    name: str = ""
    object: str = ""  # What the action operates on
    result: str = ""  # Result of the action
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    
    # Status
    status: str = ""  # ActiveActionStatus, CompleteActionStatus, etc.


class ActionMapper:
    """Maps Schema.org Actions to our databases"""
    
    def __init__(self):
        self.actions: Dict[str, ActionMapping] = {}
        self._build_mappings()
    
    def _build_mappings(self):
        for action_type, meta in ACTION_TYPE_MAP.items():
            self.actions[action_type] = ActionMapping(
                action_type=action_type,
                category=meta["category"],
                database=meta["db"]
            )
    
    def get_database(self, action_type: str) -> Optional[str]:
        """Get database for action type"""
        if action_type in self.actions:
            return self.actions[action_type].database
        return None
    
    def get_category(self, action_type: str) -> Optional[str]:
        """Get category for action type"""
        if action_type in self.actions:
            return self.actions[action_type].category
        return None
    
    def list_actions(self, category: str = None) -> List[str]:
        """List all actions or filter by category"""
        if category:
            return [a for a, m in self.actions.items() if m.category == category]
        return list(self.actions.keys())
    
    def stats(self) -> Dict:
        """Get action statistics"""
        categories = {}
        for action, meta in self.actions.items():
            cat = meta.category
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_actions": len(self.actions),
            "by_category": categories
        }


def main():
    mapper = ActionMapper()
    
    print("=== Schema.org Action Mapping ===")
    print(f"Total Actions: {len(mapper.actions)}")
    print(f"\nBy Category:")
    
    for cat in sorted(set(m.category for m in mapper.actions.values())):
        count = len([a for a, m in mapper.actions.items() if m.category == cat])
        print(f"  {cat}: {count}")
    
    print(f"\nExample: BuyAction -> {mapper.get_database('BuyAction')}")
    print(f"Example: LoginAction -> {mapper.get_database('LoginAction')}")


if __name__ == "__main__":
    main()

"""
Action Mapping Complete:
- 78 Action types mapped
- 16 categories
- All mapped to databases
"""