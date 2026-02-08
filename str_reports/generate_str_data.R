library(tidyverse)
library(lubridate)

set.seed(42)

generate_str_data <- function(market, base_adr, base_occ, n_months = 12) {
  
  # Property aliases
  property_name <- ifelse(market == "Jakarta", "Property_JKT_001", "Property_BAL_001")
  
  # Date range
  dates <- seq(ymd("2024-01-01"), by = "month", length.out = n_months)
  
  # Seasonality patterns
  if (market == "Jakarta") {
    # Corporate-driven: lower in Dec/Jan/Jul/Aug (holidays)
    seasonal_factor <- c(0.85, 0.88, 0.95, 1.00, 1.02, 0.92, 0.85, 0.87, 1.00, 1.05, 1.03, 0.82)
  } else {
    # Bali leisure: higher in Jun-Sep, Dec-Jan (peak season)
    seasonal_factor <- c(1.10, 1.08, 0.95, 0.92, 0.90, 1.05, 1.15, 1.18, 1.12, 0.95, 0.98, 1.15)
  }
  
  # Generate data for each month
  data <- tibble(
    month = dates,
    year = year(month),
    month_name = month(month, label = TRUE, abbr = FALSE)
  ) %>%
    mutate(
      # Your Property metrics
      property_rooms_available = 300 * days_in_month(month),
      property_occupancy = pmin(95, pmax(55, base_occ * seasonal_factor[row_number()] + rnorm(n(), 0, 3))),
      property_rooms_sold = round(property_rooms_available * property_occupancy / 100),
      property_adr = round(base_adr * seasonal_factor[row_number()] * rnorm(n(), 1, 0.05), -3),
      property_revpar = round(property_adr * property_occupancy / 100, -3),
      
      # Competitive Set (slightly better performance)
      compset_occupancy = property_occupancy * rnorm(n(), 1.05, 0.03),
      compset_adr = property_adr * rnorm(n(), 1.08, 0.04),
      compset_revpar = round(compset_adr * compset_occupancy / 100, -3),
      
      # Market (broader, slightly lower)
      market_occupancy = property_occupancy * rnorm(n(), 0.93, 0.05),
      market_adr = property_adr * rnorm(n(), 0.95, 0.06),
      market_revpar = round(market_adr * market_occupancy / 100, -3),
      
      # STR Indices (Key Performance Indicators)
      mpi = round((property_occupancy / compset_occupancy) * 100, 1),  # Market Penetration Index
      ari = round((property_adr / compset_adr) * 100, 1),              # Average Rate Index
      rgi = round((property_revpar / compset_revpar) * 100, 1),        # Revenue Generation Index
      
      # Segment Mix (%)
      seg_transient = ifelse(market == "Jakarta", 
                             rnorm(n(), 35, 5), 
                             rnorm(n(), 70, 5)),
      seg_group = ifelse(market == "Jakarta", 
                         rnorm(n(), 45, 5), 
                         rnorm(n(), 20, 5)),
      seg_contract = 100 - seg_transient - seg_group,
      
      # Month-over-Month change
      mom_occ_change = c(NA, diff(property_occupancy)),
      mom_adr_change = c(NA, diff(property_adr) / head(property_adr, -1) * 100),
      mom_revpar_change = c(NA, diff(property_revpar) / head(property_revpar, -1) * 100)
    ) %>%
    mutate(
      property_name = property_name,
      market = market,
      .before = 1
    ) %>%
    select(
      property_name, market, month, year, month_name,
      property_rooms_available, property_rooms_sold, property_occupancy,
      property_adr, property_revpar,
      compset_occupancy, compset_adr, compset_revpar,
      market_occupancy, market_adr, market_revpar,
      mpi, ari, rgi,
      seg_transient, seg_group, seg_contract,
      mom_occ_change, mom_adr_change, mom_revpar_change
    )
  
  return(data)
}

# Generate Jakarta data (Corporate market)
jakarta_data <- generate_str_data(
  market = "Jakarta",
  base_adr = 3500000,  # ~$225 USD
  base_occ = 72
)

# Generate Bali data (Leisure resort market)
bali_data <- generate_str_data(
  market = "Bali",
  base_adr = 5000000,  # ~$320 USD
  base_occ = 78
)

# Create output directory
dir.create("data", showWarnings = FALSE)

# Export to CSV
write_csv(jakarta_data, "data/jakarta_str_2024.csv")
write_csv(bali_data, "data/bali_str_2024.csv")

# Print summary
cat("\n=== STR Data Generated ===\n\n")
cat("Jakarta Summary:\n")
print(summary(jakarta_data %>% select(property_occupancy, property_adr, property_revpar, mpi, ari, rgi)))
cat("\nBali Summary:\n")
print(summary(bali_data %>% select(property_occupancy, property_adr, property_revpar, mpi, ari, rgi)))
cat("\n✓ Files saved to data/ directory\n")
