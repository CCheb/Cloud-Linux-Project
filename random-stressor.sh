#!/bin/bash

# Function to generate random timeout between a given range (in seconds)
random_timeout() {
    echo $((RANDOM % 30 + 10))  # Random timeout between 10 and 40 seconds
}

# Function to randomly select a stressor and its parameters
run_stressor() {
    local stressor=$1
    local timeout=$2

    case $stressor in
        "cpu")
            echo "Running CPU stress for $timeout seconds"
            stress-ng --cpu 4 --timeout ${timeout}s
            ;;
        "memory")
            echo "Running memory stress for $timeout seconds"
            stress-ng --vm 1 --vm-bytes 1G --timeout ${timeout}s
            ;;
        "io")
            echo "Running I/O stress for $timeout seconds"
            stress-ng --iomix 4 --timeout ${timeout}s
            ;;
        "filesystem")
            echo "Running filesystem stress for $timeout seconds"
            stress-ng --dir 4 --timeout ${timeout}s
            ;;
        "network")
            echo "Running network stress for $timeout seconds"
            stress-ng --netdev 4 --timeout ${timeout}s
            ;;
        *)
            echo "Unknown stressor: $stressor"
            ;;
    esac
}

# List of stressors to choose from
stressors=("cpu" "memory" "io" "filesystem" "network")

# Main loop to alternate between different stressors
while true; do
    # Randomly choose a stressor from the list
    stressor=${stressors[$RANDOM % ${#stressors[@]}]}

    # Generate a random timeout between 10 and 40 seconds
    timeout=$(random_timeout)

    # Run the selected stressor
    run_stressor $stressor $timeout

    # Sleep for a short period before switching to the next stressor
    sleep 5
done

