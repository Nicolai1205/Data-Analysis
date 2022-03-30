-- ALL OF IT
SELECT *
FROM Covid_Deaths2
Where continent is not null
Order by 3,4

-- Looking at total cases vs Total Deaths
-- Show likelyhood of duying if you contract covid in your country
Select location, date, total_cases, total_deaths, ((total_deaths*1.0)/total_cases)*100 as DeathPercentage
FROM Covid_Deaths2
Where location like "%Denmark%"
order by 1,2


-- Looking at Total Cases vs population
Select location, date, total_cases, population, ((total_cases*1.0)/population)*100 as PopulationInfection
FROM Covid_Deaths2
Where location like "%Denmark%" and Where continent is not null
order by 1,2

-- Looking at which country has highest infection rate compared to population
Select location, MAX(total_cases) as HighestInfectionCount, population, Max(((total_cases*1.0)/population))*100 as PercentageOfPopulationInfected
FROM Covid_Deaths2
--Where location like "%Denmark%"
Where continent is not null
Group by location, population
order by PercentageOfPopulationInfected DESC


-- Looking at countries with highest death count per population
Select location, MAX(CAST(total_deaths as int)) as HighestDeathCount, population, Max(((total_deaths*1.0)/population))*100 as PercentageOfPopulationDeaths
FROM Covid_Deaths2
--Where location like "%Denmark%"
Where continent is not null
Group by location, population
order by PercentageOfPopulationDeaths DESC


-- Breaking data down by continent = is not NULL
Select continent, MAX(CAST(total_deaths as int)) as HighestDeathCount, population, Max(((total_deaths*1.0)/population))*100 as PercentageOfPopulationDeaths
FROM Covid_Deaths2
--Where location like "%Denmark%"
Where continent is not null --Potenially more correct results when using "is null" instead. Example below.
Group by continent
order by PercentageOfPopulationDeaths DESC



-- Breaking data down by location (continent) = is NULL
Select location, MAX(CAST(total_deaths as int)) as TotalDeathCount, population, Max(((total_deaths*1.0)/population))*100 as PercentageOfPopulationDeaths
FROM Covid_Deaths2
--Where location like "%Denmark%"
Where continent is null AND location NOT like "%income%" -- suddenly includes locations such as "upper middle income, etc." so I excluded them. But what are they?
Group by location
order by PercentageOfPopulationDeaths DESC


-- Breaking data down by continent and showing continent with highest death percentage
Select continent, MAX(CAST(total_deaths as int)) as TotalDeathCount, population, Max(((total_deaths*1.0)/population))*100 as PercentageOfPopulationDeaths
FROM Covid_Deaths2
--Where location like "%Denmark%"
Where continent is not null AND location NOT like "%income%" -- includes locations such as "upper middle income, etc." so I excluded them. But what are they?
Group by continent
order by PercentageOfPopulationDeaths DESC


-- Global Numbers
Select sum(new_cases) as TotalCases, SUM(cast(new_deaths as int)) as TotalDeaths, sum(new_deaths*1.0)/sum(new_cases)*100 as DeathPercentageGlobal
FROM Covid_Deaths2
Where continent is not null
--GROUP by date
order by 1,2


--Total population vs vaccinations
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
,SUM(CAST(vac.new_vaccinations as INT)) OVER (PARTITION by dea.location order by dea.location, dea.date) as CumulativeSumVaccinated
--,(CumulativeSumVaccinated/population)*100
FROM Covid_Deaths2 dea
JOIN Covid_Vaccines2 vac
	On dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not NULL
order by 2,3


-- USE CTE
With PopvsVac (Continent, Location, Date, Population, new_vaccinations, CumulativeSumVaccinated)
as
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
,SUM(CAST(vac.new_vaccinations as INT)) OVER (PARTITION by dea.location order by dea.location, dea.date) as CumulativeSumVaccinated
FROM Covid_Deaths2 dea
JOIN Covid_Vaccines2 vac
	On dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not NULL
)
Select *, (CumulativeSumVaccinated*1.0/population)*100 as CumSumVaccinatedOfPop
FROM PopvsVac


-- TEMP TABLE
Drop TABLE if exists PercentPopulationVaccinated --Needs to be executed by itself in SQLITE
CREATE TABLE PercentPopulationVaccinated--Needs to be executed by itself in SQLITE
(
continent varchar(255),
location varchar(255),
date datetime,
population numeric,
new_vaccinations numeric,
CumulativeSumVaccinated NUMERIC
);

Insert INTO PercentPopulationVaccinated --This and Below Needs to be executed by itself in SQLITE
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
,SUM(CAST(vac.new_vaccinations as INT)) OVER (PARTITION by dea.location order by dea.location, dea.date) as CumulativeSumVaccinated
FROM Covid_Deaths2 dea
JOIN Covid_Vaccines2 vac
	On dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not NULL

--Needs to be executed by itself in SQLITE
Select *, (CumulativeSumVaccinated*1.0/population)*100
FROM PercentPopulationVaccinated



-- Creating view for storing data to visualize

CREATE VIEW PercentPopulationVaccinatedView as
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
,SUM(CAST(vac.new_vaccinations as INT)) OVER (PARTITION by dea.location order by dea.location, dea.date) as CumulativeSumVaccinated
FROM Covid_Deaths2 dea
JOIN Covid_Vaccines2 vac
	On dea.location = vac.location
	and dea.date = vac.date
Where dea.continent is not NULL

--Select the newly created VIEW
Select *
From PercentPopulationVaccinatedView