"""
Agent Consumer - How Agents Use All Databases

This module shows how an Agent (SoftwareApplication) can consume/use all databases:
- Query knowledge graph for context
- Search movie database for recommendations
- Access sports data for analysis
- Use healthcare for wellness
- Process orders from e-commerce

Reference: Agent Platform consumption patterns
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime


# =============================================================================
# AGENT CONSUMER CLASSES
# =============================================================================

@dataclass
class AgentConsumer:
    """
    A consuming agent that uses all databases
    
    This shows how an AI Agent (SoftwareApplication) can:
    1. Query knowledge from knowledge graph
    2. Search movies for recommendations
    3. Access sports data
    4. Use healthcare info
    5. Manage e-commerce orders
    """
    
    # Agent identity
    agent_id: str
    name: str
    
    # Connected databases
    knowledge_graph: Any = None
    movie_db: Any = None
    sports_db: Any = None
    healthcare_db: Any = None
    restaurant_db: Any = None
    music_db: Any = None
    real_estate_db: Any = None
    ecommerce_db: Any = None
    education_db: Any = None
    
    # Skills/Capabilities
    skills: List[str] = field(default_factory=list)
    
    # Memory
    conversation_history: List[Dict] = field(default_factory=list)
    long_term_memory: List[Dict] = field(default_factory=list)
    
    # Configuration
    auto_search: bool = True
    context_window: int = 5
    
    # Connect databases
    def connect_knowledge_graph(self, db):
        """Connect to knowledge graph"""
        self.knowledge_graph = db
        self.skills.append("knowledge_query")
        return self
    
    def connect_movie_db(self, db):
        """Connect to movie database"""
        self.movie_db = db
        self.skills.append("movie_recommend")
        return self
    
    def connect_sports_db(self, db):
        """Connect to sports database"""
        self.sports_db = db
        self.skills.append("sports_analysis")
        return self
    
    def connect_healthcare_db(self, db):
        """Connect to healthcare database"""
        self.healthcare_db = db
        self.skills.append("healthcare_query")
        return self
    
    def connect_ecommerce_db(self, db):
        """Connect to e-commerce database"""
        self.ecommerce_db = db
        self.skills.append("order_management")
        return self
    
    # =================================================================
    # CONSUME KNOWLEDGE GRAPH
    # =================================================================
    
    def queryKnowledge(self, query: str) -> List[Dict]:
        """Query the knowledge graph"""
        if not self.knowledge_graph:
            return [{"error": "No knowledge graph connected"}]
        
        results = self.knowledge_graph.search(query)
        
        # Store in memory
        self.long_term_memory.append({
            "type": "knowledge_query",
            "query": query,
            "results": results,
            "timestamp": datetime.now().isoformat()
        })
        
        return results
    
    def getPersonInfo(self, name: str) -> Dict:
        """Get person info from Wikipedia"""
        if not self.knowledge_graph:
            return {}
        
        return self.knowledge_graph.get_person(name)
    
    def buildPersonGraph(self, name: str, depth: int = 2) -> int:
        """Build knowledge graph for a person"""
        if not self.knowledge_graph:
            return 0
        
        return self.knowledge_graph.build_from_seed(name, depth)
    
    # =================================================================
    # CONSUME MOVIE DATABASE
    # =================================================================
    
    def searchMovies(self, query: str) -> List[Dict]:
        """Search movies"""
        if not self.movie_db:
            return [{"error": "No movie database connected"}]
        
        return self.movie_db.search_movie(query)
    
    def getMovieRecommendations(self, genre: str = None, year: int = None) -> List[Dict]:
        """Get movie recommendations"""
        if not self.movie_db:
            return []
        
        movies = self.movie_db.movies.values()
        
        if genre:
            movies = [m for m in movies if genre in m.genres]
        
        if year:
            movies = [m for m in movies if m.release_date and m.release_date.year == year]
        
        # Sort by rating
        movies = sorted(movies, key=lambda m: m.imdb_rating or 0, reverse=True)
        
        return [{"title": m.title, "rating": m.imdb_rating, "year": str(m.release_date)[:4] for m in movies[:10]]
    
    def getActorInfo(self, name: str) -> Dict:
        """Get actor info"""
        if not self.movie_db:
            return {}
        
        actors = self.movie_db.search_person(name)
        if actors:
            return {
                "name": actors[0].name,
                "total_movies": actors[0].total_movies,
                "known_for": actors[0].known_for
            }
        return {}
    
    def getMovieReviews(self, movie_id: str) -> List[Dict]:
        """Get movie reviews"""
        if not self.movie_db:
            return []
        
        return self.movie_db.get_movie_reviews(movie_id)
    
    # =================================================================
    # CONSUME SPORTS DATABASE
    # =================================================================
    
    def getTeamInfo(self, team_id: str) -> Dict:
        """Get team info"""
        if not self.sports_db:
            return {}
        
        team = self.sports_db.get_team(team_id)
        if not team:
            return {}
        
        return {
            "name": team.name,
            "league": team.league.value,
            "wins": team.wins,
            "losses": team.losses,
            "win_pct": team.win_pct()
        }
    
    def getAthleteStats(self, athlete_id: str) -> Dict:
        """Get athlete statistics"""
        if not self.sports_db:
            return {}
        
        athlete = self.sports_db.get_athlete(athlete_id)
        if not athlete:
            return {}
        
        return {
            "name": athlete.name,
            "position": athlete.position.value if athlete.position else None,
            "team_id": athlete.team_id,
            "jersey_number": athlete.jersey_number,
            "height_cm": athlete.height_cm,
            "weight_kg": athlete.weight_kg
        }
    
    def getGameScore(self, game_id: str) -> Dict:
        """Get game score"""
        if not self.sports_db:
            return {}
        
        game = self.sports_db.get_game(game_id)
        if not game:
            return {}
        
        return {
            "home": game.home_team_id,
            "away": game.away_team_id,
            "home_score": game.home_score,
            "away_score": game.away_score,
            "status": game.status.value
        }
    
    def getUpcomingGames(self, limit: int = 10) -> List[Dict]:
        """Get upcoming games"""
        if not self.sports_db:
            return []
        
        return self.sports_db.get_upcoming_games(limit)
    
    def getLeagueStandings(self, league) -> List[Dict]:
        """Get league standings"""
        if not self.sports_db:
            return []
        
        standings = self.sports_db.get_league_standings(league)
        
        return [{"rank": i+1, "name": t.name, "wins": t.wins, "losses": t.losses} 
                for i, t in enumerate(standings)]
    
    # =================================================================
    # CONSUME HEALTHCARE DATABASE
    # =================================================================
    
    def findPhysician(self, specialty: str = None) -> List[Dict]:
        """Find physicians"""
        if not self.healthcare_db:
            return []
        
        physicians = self.healthcare_db.physicians.values()
        
        if specialty:
            physicians = [p for p in physicians if p.specialty and p.specialty.value == specialty]
        
        return [{"name": d.name, "specialty": d.specialty.value if d.specialty else None} for d in physicians]
    
    def getPatientInfo(self, patient_id: str) -> Dict:
        """Get patient info"""
        if not self.healthcare_db:
            return {}
        
        patient = self.healthcare_db.patients.get(patient_id)
        if not patient:
            return {}
        
        return {
            "name": patient.name,
            "birth_date": str(patient.birth_date) if patient.birth_date else None,
            "allergies": patient.allergies,
            "conditions": patient.conditions
        }
    
    def scheduleAppointment(
        self, 
        patient_id: str, 
        physician_id: str, 
        facility_id: str,
        time: datetime
    ) -> str:
        """Schedule appointment"""
        if not self.healthcare_db:
            return "No database connected"
        
        from additional_databases import Appointment
        appt = Appointment(
            id=f"appt-{patient_id}-{physician_id}",
            patient_id=patient_id,
            physician_id=physician_id,
            facility_id=facility_id,
            scheduled_time=time
        )
        
        return self.healthcare_db.add_appointment(appt)
    
    def getAppointments(self, patient_id: str = None, physician_id: str = None) -> List[Dict]:
        """Get appointments"""
        if not self.healthcare_db:
            return []
        
        if patient_id:
            appts = self.healthcare_db.get_patient_appointments(patient_id)
        elif physician_id:
            appts = self.healthcare_db.get_physician_schedule(physician_id)
        else:
            return []
        
        return [{"id": a.id, "time": str(a.scheduled_time), "status": a.status.value} for a in appts]
    
    # =================================================================
    # CONSUME E-COMMERCE
    # =================================================================
    
    def searchProducts(self, query: str) -> List[Dict]:
        """Search products"""
        if not self.ecommerce_db:
            return []
        
        # Search would need implementation
        return []
    
    def createOrder(self, customer_id: str, items: List[Dict]) -> str:
        """Create order"""
        if not self.ecommerce_db:
            return "No database connected"
        
        from additional_databases import Order
        order = Order(
            id=f"order-{customer_id}-{len(items)}",
            customer_id=customer_id,
            items=items,
            total=sum(i.get("price", 0) * i.get("quantity", 1) for i in items)
        )
        
        return order.id
    
    def getOrderStatus(self, order_id: str) -> Dict:
        """Get order status"""
        if not self.ecommerce_db:
            return {}
        
        return {"order_id": order_id, "status": "Processing"}
    
    def trackShipment(self, tracking_number: str) -> Dict:
        """Track shipment"""
        return {
            "tracking": tracking_number,
            "status": "In Transit",
            "location": "Distribution Center"
        }
    
    # =================================================================
    # CONSUME ALL DATABASES - UNIFIED
    # =================================================================
    
    def consume(self, query: str, context: str = None) -> Dict:
        """
        Main method: Consume query across all databases
        
        Automatically determines which database to use based on query
        """
        response = {
            "query": query,
            "agent": self.name,
            "timestamp": datetime.now().isoformat()
        }
        
        query_lower = query.lower()
        
        # Knowledge Graph
        if any(kw in query_lower for kw in ["who is", "what is", "tell me about", "information"]):
            results = self.queryKnowledge(query)
            response["source"] = "knowledge_graph"
            response["results"] = results
        
        # Movies
        elif any(kw in query_lower for kw in ["movie", "film", "actor", "director", "watch"]):
            results = self.searchMovies(query)
            response["source"] = "movie_database"
            response["results"] = results
        
        # Sports
        elif any(kw in query_lower for kw in ["team", "player", "game", "score", "win", "loss"]):
            if self.sports_db:
                response["source"] = "sports_database"
                response["results"] = []
        
        # Healthcare
        elif any(kw in query_lower for kw in ["doctor", "hospital", "appointment", "medical"]):
            if self.healthcare_db:
                response["source"] = "healthcare_database"
                response["results"] = []
        
        # E-commerce
        elif any(kw in query_lower for kw in ["order", "buy", "product", "price"]):
            results = self.searchProducts(query)
            response["source"] = "ecommerce"
            response["results"] = results
        
        # Default
        else:
            response["source"] = "general"
            response["results"] = [{"message": "I can help with movies, sports, healthcare, and more!"}]
        
        # Store in conversation
        self.conversation_history.append({
            "query": query,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Trim history
        if len(self.conversation_history) > self.context_window:
            self.conversation_history = self.conversation_history[-self.context_window:]
        
        return response
    
    def getContext(self) -> List[Dict]:
        """Get conversation context"""
        return self.conversation_history
    
    def getMemory(self) -> List[Dict]:
        """Get long-term memory"""
        return self.long_term_memory


# =============================================================================
# EXAMPLE: CONSUMING ALL DATABASES
# =============================================================================

def main():
    """Example - Agent consuming all databases"""
    
    print("=" * 60)
    print("Agent Consuming All Databases")
    print("=" * 60)
    
    # Create consuming agent
    agent = AgentConsumer(
        agent_id="agent-001",
        name="Multi-DB Assistant",
        skills=["knowledge_query", "movie_recommend", "sports_analysis"]
    )
    
    # Connect databases (would import real ones in production)
    # agent.connect_knowledge_graph(knowledge_graph)
    # agent.connect_movie_db(movie_db)
    # agent.connect_sports_db(sports_db)
    # agent.connect_healthcare_db(healthcare_db)
    # agent.connect_ecommerce_db(ecommerce_db)
    
    print(f"\n1. Agent: {agent.name}")
    print(f"   Skills: {agent.skills}")
    
    # Query examples
    print("\n2. Query Knowledge Graph:")
    result = agent.consume("Who is Elon Musk?")
    print(f"   Query: {result['query']}")
    print(f"   Source: {result['source']}")
    
    print("\n3. Query Movies:")
    result = agent.consume("Find good action movies")
    print(f"   Source: {result['source']}")
    
    print("\n4. Query Sports:")
    result = agent.consume("What's the Lakers score?")
    print(f"   Source: {result['source']}")
    
    print("\n5. Healthcare:")
    result = agent.consume("Find a cardiologist")
    print(f"   Source: {result['source']}")
    
    print("\n6. E-commerce:")
    result = agent.consume("Order running shoes")
    print(f"   Source: {result['source']}")
    
    # Context
    print("\n7. Conversation Context:")
    context = agent.getContext()
    print(f"   History: {len(context)} queries")


if __name__ == "__main__":
    main()


"""
Agent Consumer Usage

    # Create agent
    agent = AgentConsumer(
        agent_id="agent-001",
        name="Multi-DB Assistant"
    )
    
    # Connect databases
    agent.connect_knowledge_graph(kg_db)
    agent.connect_movie_db(movie_db)
    agent.connect_sports_db(sports_db)
    agent.connect_healthcare_db(healthcare_db)
    agent.connect_ecommerce_db(ecommerce_db)
    
    # Query any database
    result = agent.consume("Who is Elon Musk?")
    result = agent.consume("Find good sci-fi movies")
    result = agent.consume("Get Lakers game score")
    result = agent.consume("Find cardiologist")
    result = agent.consume("Order shoes")
    
    # Direct access
    agent.queryKnowledge("Elon Musk")
    agent.searchMovies("Inception")
    agent.getTeamInfo("t1")
    agent.findPhysician("Cardiology")
    agent.createOrder("customer-1", items)

Each database is consumed via the unified consume() method!
"""