import os
import json
from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperDevTool,
	ScrapeWebsiteTool
)






@CrewBase
class AiTravelItineraryPlannerCrew:
    """AiTravelItineraryPlanner crew"""

    
    @agent
    def travel_destination_research_specialist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["travel_destination_research_specialist"],
            
            
            tools=[
				# SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gemini/gemini-2.0-flash",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def accommodation_and_transportation_coordinator(self) -> Agent:

        
        return Agent(
            config=self.agents_config["accommodation_and_transportation_coordinator"],
            
            
            tools=[
				# SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gemini/gemini-2.0-flash",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def local_experience_and_activity_curator(self) -> Agent:

        
        return Agent(
            config=self.agents_config["local_experience_and_activity_curator"],
            
            
            tools=[
				# SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gemini/gemini-2.0-flash",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def master_itinerary_planner(self) -> Agent:

        
        return Agent(
            config=self.agents_config["master_itinerary_planner"],
            
            
            tools=[
				ScrapeWebsiteTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gemini/gemini-2.0-flash",
                temperature=0.7,
            ),
            
        )
    

    
    @task
    def research_destination_information(self) -> Task:
        return Task(
            config=self.tasks_config["research_destination_information"],
            markdown=False,
            
            
        )
    
    @task
    def find_accommodations_and_transportation(self) -> Task:
        return Task(
            config=self.tasks_config["find_accommodations_and_transportation"],
            markdown=False,
            
            
        )
    
    @task
    def curate_local_experiences_and_dining(self) -> Task:
        return Task(
            config=self.tasks_config["curate_local_experiences_and_dining"],
            markdown=False,
            
            
        )
    
    @task
    def create_complete_travel_itinerary(self) -> Task:
        return Task(
            config=self.tasks_config["create_complete_travel_itinerary"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the AiTravelItineraryPlanner crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    # def _load_response_format(self, name):
    #     with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
    #         json_schema = json.loads(f.read())

    #     return SchemaConverter.build(json_schema)
    
    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json"), "r") as f:
            json_schema = json.load(f)
        return json_schema
