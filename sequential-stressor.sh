#!/bin/bash

# Function to generate random timeout between a given range (in seconds)
random_timeout() {
    echo $((RANDOM % 30 + 10))  # Random timeout between 10 and 40 seconds
}

# Function to run a selected stressor
run_stressor() {
    local stressor=$1
    local timeout=$2

    case $stressor in
        "memory")
            echo "Running memory stress for $timeout seconds"
            stress-ng --vm 1 --vm-bytes 1G --timeout ${timeout}s
            ;;
        "cpu")
            echo "Running CPU stress for $timeout seconds"
            stress-ng --cpu 4 --timeout ${timeout}s
            ;;
        "io")
            echo "Running I/O stress for $timeout seconds"
            stress-ng --hdd 1 --aggressive --timeout ${timeout}s
            ;;
        "filesystem")
            echo "Running filesystem stress for $timeout seconds"
            stress-ng --dir 1 --aggressive  --timeout ${timeout}s
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

# List of stressors in sequential order
stressors=("memory" "cpu" "io" "filesystem" "network")

# Initialize a counter to track the current stressor
counter=0

# Main loop to cycle through stressors sequentially
while true; do
    # Get the current stressor based on the counter
    stressor=${stressors[$counter]}

    # Generate a random timeout between 10 and 40 seconds
    timeout=$(random_timeout)

    # Run the selected stressor
    run_stressor $stressor $timeout

    # Sleep for a short period before switching to the next stressor
    sleep 5

    # Increment the counter and loop back to the start if we reach the end of the list
    ((counter++))
    if [ $counter -ge ${#stressors[@]} ]; then
        counter=0
    fi
done

