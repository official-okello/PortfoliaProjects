select * from coviddeaths
order by 3,4;

-- select * from covidvaccinations
-- order by 3,4;

select Location, date, total_cases, new_cases, total_deaths, population
from coviddeaths
order by 1,2
;

-- Total cases vs Total deaths-- 
-- Likelihood of dying if you contract covid in Kenya --
select Location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
from coviddeaths
where Location = 'kenya'
order by 1,2
;

-- Total cases vs population
-- Percentage of population that has covid
select Location, date, population, total_cases, (total_cases/population)*100 as InfectionPercentage
from coviddeaths
where Location = 'kenya'
order by 1,2
;

-- Locations with highest death count compared to population
select Location, max(coalesce(cast(total_deaths as float), 0)) as TotalDeathCount
from coviddeaths
group by Location
order by TotalDeathCount desc
;

-- Countries with highest infection rate compared to population
select Location, population, max(total_cases) as HighestInfectionCoount, max((total_cases/population))*100 as InfectionPercentage
from coviddeaths
group by Location, population
order by InfectionPercentage desc
;

-- Total Deaths by continent
select continent, max(coalesce(cast(total_deaths as float), 0)) as TotalDeathCount
from coviddeaths
where continent is not null
group by continent
order by TotalDeathCount desc
;

-- Global Numbers
select date, sum(new_cases) as total_cases, sum(cast(new_deaths as float)) as total_deaths, (sum(cast(new_deaths as float))/sum(new_cases))*100 as DeathPercentage --
from coviddeaths
where continent is not null
group by date
order by 1,2
;

select sum(new_cases) as total_cases, sum(cast(new_deaths as float)) as total_deaths, (sum(cast(new_deaths as float))/sum(new_cases))*100 as DeathPercentage --
from coviddeaths
where continent is not null
order by 1,2
;

-- Both tables
-- Total vaccination vs population
select d.continent, d.location, d.date, d.population, v.new_vaccinations, sum(cast(v.new_vaccinations as float)) over (partition by d.location order by d.date) as rolling_vac_count
from coviddeaths d
join covidvaccinations v
on d.location = v.location and d.date = v.date
order by 2,3
;

-- Using CTE
with PopVsVac (Continent, Location, Date, Population, New_vaccinations, Rolling_vac_count)
as (
select d.continent, d.location, d.date, d.population, v.new_vaccinations, sum(cast(v.new_vaccinations as float)) over (partition by d.location order by d.date) as rolling_vac_count
from coviddeaths d
join covidvaccinations v
on d.location = v.location and d.date = v.date
)
select *, (Rolling_vac_count/Population)*100
from PopVsVac
;

-- Using TEMP table
-- Drop temp table if exists
DROP TEMPORARY TABLE IF EXISTS popvsvac;

-- Creating temp table
CREATE TEMPORARY TABLE popvsvac (
    Continent           VARCHAR(255),
    Location            VARCHAR(255),
    Date_               DATE,
    Population          BIGINT,
    New_vaccinations    BIGINT,
    Rolling_vac_count   DECIMAL(18,2)
);

-- Inserting cleaned data
INSERT INTO popvsvac
SELECT 
    d.Continent, 
    d.Location, 
    STR_TO_DATE(d.Date, '%m/%d/%Y') AS Date_,
    CAST(NULLIF(d.Population, '') AS UNSIGNED), 
    CAST(NULLIF(vax.New_vaccinations, '') AS UNSIGNED),
    SUM(CAST(COALESCE(NULLIF(vax.New_vaccinations, ''), '0') AS DECIMAL(18,2)))
        OVER (PARTITION BY d.Location ORDER BY STR_TO_DATE(d.Date, '%m/%d/%Y')) AS rolling_vac_count
FROM coviddeaths d
JOIN covidvaccinations vax
    ON d.Location = vax.Location 
   AND STR_TO_DATE(d.Date, '%m/%d/%Y') = STR_TO_DATE(vax.Date, '%m/%d/%Y');

-- select from the temp table
SELECT 
    *, 
    ROUND((Rolling_vac_count / NULLIF(Population, 0)) * 100, 2) AS Percent_Vaccinated
FROM popvsvac;

-- create view
create view popvsvac as
SELECT 
    d.Continent, 
    d.Location, 
    STR_TO_DATE(d.Date, '%m/%d/%Y') AS Date_,
    CAST(NULLIF(d.Population, '') AS UNSIGNED), 
    CAST(NULLIF(vax.New_vaccinations, '') AS UNSIGNED),
    SUM(CAST(COALESCE(NULLIF(vax.New_vaccinations, ''), '0') AS DECIMAL(18,2)))
        OVER (PARTITION BY d.Location ORDER BY STR_TO_DATE(d.Date, '%m/%d/%Y')) AS rolling_vac_count
FROM coviddeaths d
JOIN covidvaccinations vax
    ON d.Location = vax.Location 
   AND STR_TO_DATE(d.Date, '%m/%d/%Y') = STR_TO_DATE(vax.Date, '%m/%d/%Y');
   
-- select from view
select *
from popvsvac;