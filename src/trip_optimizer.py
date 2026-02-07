import math


def calculate_car_trip(distance_one_way, speed_kmh, efficiency_kml, max_hours_per_day, gas_price, toll_one_way,
                       is_round_trip):
    """
    Calculates trip details.
    - Costs are TOTAL (Round trip if selected).
    - Stops are ONE WAY (for clarity).
    """
    # --- 1. CONSTANTS & CONFIG ---
    REST_HOURS_PER_NIGHT = 10
    TOLERANCE_KM = 50  # If destination is within 50km, don't stop. Drive it!

    # --- 2. PREPARE DISTANCES ---
    if is_round_trip:
        total_distance_for_cost = distance_one_way * 2
        total_toll_cost = toll_one_way * 2
    else:
        total_distance_for_cost = distance_one_way
        total_toll_cost = toll_one_way

    # --- 3. FINANCIAL CALCULATION (Always Total) ---
    driving_time_hours_total = total_distance_for_cost / speed_kmh
    fuel_needed_liters = total_distance_for_cost / efficiency_kml
    fuel_cost = fuel_needed_liters * gas_price
    total_trip_cost = fuel_cost + total_toll_cost

    # --- 4. STOP LOGIC (Based on ONE WAY only) ---
    # We calculate stops for just one leg. If it's round trip, the user repeats them on the way back.
    daily_range_km = speed_kmh * max_hours_per_day

    current_km = 0
    stops_at_km = []

    # We check against ONE WAY distance
    # LOGIC: Only add a stop if the remaining distance is GREATER than range + tolerance.
    # Example: If range is 800, and we are at 0.
    # If distance is 802... (802 > 800+50?) -> False. No stop. Just finish.
    # If distance is 2402...
    #   1. Current 0. Remainder 2402. > 850? Yes. Add Stop at 800.
    #   2. Current 800. Remainder 1602. > 850? Yes. Add Stop at 1600.
    #   3. Current 1600. Remainder 802. > 850? NO. Don't stop at 2400. Finish at 2402.

    remaining_distance = distance_one_way

    while remaining_distance > (daily_range_km + TOLERANCE_KM):
        current_km += daily_range_km
        stops_at_km.append(current_km)
        remaining_distance -= daily_range_km

    # --- 5. DURATION CALCULATION ---
    # Nights one way
    nights_one_way = len(stops_at_km)

    if is_round_trip:
        total_nights = nights_one_way * 2
    else:
        total_nights = nights_one_way

    total_rest_hours = total_nights * REST_HOURS_PER_NIGHT
    real_total_time = driving_time_hours_total + total_rest_hours

    return {
        "fuel_cost": fuel_cost,
        "toll_cost": total_toll_cost,
        "total_cost": total_trip_cost,
        "stops_one_way": stops_at_km,  # Only [800, 1600]
        "total_time_hours": real_total_time,
        "total_nights": total_nights,
        "is_round_trip": is_round_trip
    }


def main():
    print("--- 🚗 CALCULADORA DE VIAGEM (OTIMIZADOR 4.0) ---")

    try:
        # Inputs
        raw_distance = float(input("Distância (KM) - Apenas ida: "))
        speed = float(input("Velocidade Média (KM/H): "))
        efficiency = float(input("Eficiência do Carro (KM/L): "))
        gas_price = float(input("Preço da Gasolina (R$): "))
        max_hours = float(input("Horas de pilotagem por dia: "))
        toll_one_way = float(input("Custo estimado de Pedágio (Apenas Ida): "))

        # Trip Type
        trip_input = input("É ida e volta? (S/N): ").strip().upper()
        is_round_trip = (trip_input == 'S')

        # Validation
        if speed <= 0 or efficiency <= 0:
            print("❌ Erro: Velocidade e Eficiência devem ser maiores que zero.")
            return

        # Run Calculation
        result = calculate_car_trip(raw_distance, speed, efficiency, max_hours, gas_price, toll_one_way, is_round_trip)

        # Output
        print("\n--- 📊 RESULTADO FINANCEIRO ---")
        print(f"⛽ Custo Combustível: R$ {result['fuel_cost']:.2f}")
        print(f"🚧 Custo Pedágio:     R$ {result['toll_cost']:.2f}")
        print(f"💰 CUSTO TOTAL:       R$ {result['total_cost']:.2f}")

        print("\n--- ⏱️ LOGÍSTICA ---")
        if result['is_round_trip']:
            print(f"🔄 Modo: Ida e Volta")
        else:
            print(f"➡️ Modo: Apenas Ida")

        print(f"⏱️ Tempo Total (Estrada + Descanso): {result['total_time_hours']:.1f} horas")

        if result['total_nights'] > 0:
            print(f"🏨 Pernoites Totais: {result['total_nights']}")

            # Smart Display for Stops
            print(f"\n🛑 PARADAS SUGERIDAS (Apenas Ida): {result['stops_one_way']}")
            if result['is_round_trip']:
                print(f"   (Na volta, considere as mesmas paradas em ordem inversa)")
        else:
            print("✅ Viagem direta (Sem necessidade de pernoite).")

    except ValueError:
        print("\n❌ ERRO: Digite apenas números.")
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")


if __name__ == "__main__":
    main()