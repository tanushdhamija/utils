from psutil import cpu_percent, virtual_memory, disk_usage
import subprocess
import time

def get_system_stats():
    try:
        # Run nvidia-smi query for multiple GPUs
        result = subprocess.run([
            "nvidia-smi",
            "--query-gpu=utilization.gpu,memory.used,memory.total,power.draw,temperature.gpu",
            "--format=csv,noheader,nounits"], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # Process GPU results
        gpu_data = []
        for line in result.stdout.strip().split("\n"):
            utilization_gpu, memory_used, memory_total, power_draw, temperature_gpu = [float(x.strip()) for x in line.split(",")]
            vram_percent = memory_used / memory_total * 100
            gpu_data.append({
                'utilization_gpu': utilization_gpu,
                'vram': round(vram_percent, 2),
                'power': power_draw,
                'temperature': temperature_gpu
            })
        
        # Gather CPU, RAM, and Disk statistics
        return dict(
            cpu=cpu_percent(),
            disk=disk_usage("/").percent,
            ram=virtual_memory().percent,
            gpus=gpu_data  # List containing multiple GPU stats
        )

    except subprocess.CalledProcessError as e:
        print(f"Error executing nvidia-smi: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    while True:
        stats = get_system_stats()
        if stats:
            print(f"{'-'*30}\nCPU: {stats['cpu']}% \nDisk: {stats['disk']}% \nRAM: {stats['ram']}%")
            for i, gpu in enumerate(stats['gpus']):
                print(f"\nGPU {i}:")
                print(f"  Utilization: {gpu['utilization_gpu']}%")
                print(f"  VRAM: {gpu['vram']}%")
                print(f"  Power: {gpu['power']}W")
                print(f"  Temperature: {gpu['temperature']}°C")
        time.sleep(2)
