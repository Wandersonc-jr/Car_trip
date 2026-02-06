import math


def calculate_car_trip(distance_km, speed_kmh, efficiency_kml, max_hours_per_day):
    """
    Calculates cost and time for a car trip.
    Returns a Dictionary with the results.
    """
    # 1. Constants
    GAS_PRICE = 6.33
    REST_HOURS_PER_NIGHT = 10  # Hotel + Dinner + Breakfast

    # 2. Basic Math
    driving_time_hours = distance_km / speed_kmh
    fuel_needed_liters = distance_km / efficiency_kml
    fuel_cost = fuel_needed_liters * GAS_PRICE

    # 3. Stop Logic (The Loop)
    daily_range_km = speed_kmh * max_hours_per_day
    current_km = 0
    stops_at_km = []

    # While we still have more distance than we can drive in one day...
    remaining_distance = distance_km

    while remaining_distance > daily_range_km:
        current_km += daily_range_km
        stops_at_km.append(current_km)
        remaining_distance -= daily_range_km

    # 4. Total Duration
    nights_stopped = len(stops_at_km)
    total_rest_hours = nights_stopped * REST_HOURS_PER_NIGHT
    real_total_time = driving_time_hours + total_rest_hours

    # Return structured data
    return {
        "fuel_cost": fuel_cost,
        "stops": stops_at_km,
        "total_time_hours": real_total_time,
        "nights": nights_stopped,
        "final_distance": distance_km  # Return this so we can print it later
    }


def main():
    print("--- 🚗 CALCULADORA DE VIAGEM (OTIMIZADOR) ---")

    try:
        # Inputs
        raw_distance = float(input("Distância (KM) - Apenas ida: "))
        speed = float(input("Velocidade Média (KM/H): "))
        efficiency = float(input("Eficiência do Carro (KM/L): "))
        max_hours = float(input("Horas de pilotagem por dia: "))

        # --- NEW FEATURE: Round Trip Toggle ---
        trip_type = input("É ida e volta? (S/N): ").strip().upper()

        if trip_type == 'S':
            total_distance = raw_distance * 2
            print(f"🔄 Calculando Ida e Volta ({total_distance} KM total)...")
        else:
            total_distance = raw_distance
            print(f"➡️ Calculando Apenas Ida ({total_distance} KM total)...")

        # Validation
        if speed <= 0 or efficiency <= 0:
            print("❌ Erro: Velocidade e Eficiência devem ser maiores que zero.")
            return

        # Run Calculation with the ADJUSTED distance
        result = calculate_car_trip(total_distance, speed, efficiency, max_hours)

        # Output
        print("\n--- 📊 RESULTADO DA ANÁLISE ---")
        print(f"🛣️ Distância Total Percorrida: {result['final_distance']} km")
        print(f"💰 Preço total do combustível: R$ {result['fuel_cost']:.2f}")
        print(f"⏱️ Tempo Total de Viagem: {result['total_time_hours']:.1f} horas")

        if result['nights'] > 0:
            print(f"🏨 Pernoites Necessários: {result['nights']}")
            print(f"🛑 Sugestão de Paradas (KMs acumulados): {result['stops']}")
        else:
            print("✅ Viagem direta (Sem necessidade de pernoite).")

    except ValueError:
        print("\n❌ ERRO: Por favor, digite apenas números.")
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")


if __name__ == "__main__":
    main()