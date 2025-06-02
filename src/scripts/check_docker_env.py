#!/usr/bin/env python

import os
import sys
import subprocess
import docker
import time
import json

def check_docker_installation():
    """Check if Docker is installed and print version info"""
    try:
        docker_version = subprocess.check_output(['docker', '--version'], stderr=subprocess.STDOUT).decode('utf-8').strip()
        print(f"✅ Docker is installed: {docker_version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not installed or not in PATH")
        return False

def check_docker_running():
    """Check if Docker daemon is running"""
    try:
        client = docker.from_env()
        info = client.info()
        print(f"✅ Docker is running - {info.get('Name', 'unnamed host')}")
        print(f"   Containers: {info.get('Containers', 'unknown')}")
        print(f"   Images: {info.get('Images', 'unknown')}")
        return True
    except Exception as e:
        print(f"❌ Docker daemon is not running: {e}")
        return False

def test_mysql_container():
    """Test creating a MySQL container"""
    try:
        print("\nTesting MySQL container creation...")
        client = docker.from_env()
        
        # Test parameters
        container_name = "sql_practice_test_container"
        mysql_root_password = "test_password"
        mysql_database = "test_db"
        
        # Clean up any existing test container
        try:
            old_container = client.containers.get(container_name)
            print("   Removing existing test container...")
            old_container.remove(force=True)
        except docker.errors.NotFound:
            pass
        
        # Create container
        print("   Creating container...")
        container = client.containers.run(
            "mysql:8.0",
            name=container_name,
            detach=True,
            environment={
                "MYSQL_ROOT_PASSWORD": mysql_root_password,
                "MYSQL_DATABASE": mysql_database
            },
            ports={'3306/tcp': None}  # Auto-assign port
        )
        
        # Get container info
        print("   Container created, waiting for startup...")
        time.sleep(5)  # Brief wait for container to initiate startup
        
        container.reload()
        port = container.attrs['NetworkSettings']['Ports']['3306/tcp'][0]['HostPort']
        print(f"   Container is {container.status} on port {port}")
        
        # Wait up to 30 seconds for MySQL to be ready
        for i in range(30):
            print(f"   Checking MySQL readiness ({i+1}/30)...")
            
            # Simple check on container logs
            logs = container.logs().decode('utf-8', errors='replace')
            if "MySQL init process done. Ready for start up." in logs:
                print("   ✅ MySQL is ready!")
                break
                
            container.reload()
            if container.status != "running":
                print(f"   ❌ Container is not running: {container.status}")
                break
                
            time.sleep(1)
        else:
            print("   ⚠️ Timeout waiting for MySQL to be ready, but container is still running")
        
        # Print container details
        container.reload()
        print("\nContainer details:")
        print(f"  ID: {container.id}")
        print(f"  Name: {container.name}")
        print(f"  Status: {container.status}")
        print(f"  Port: {port}")
        
        # Clean up
        print("\nCleaning up test container...")
        container.remove(force=True)
        print("   ✅ Test container removed")
        
        return True
    except Exception as e:
        print(f"❌ Error testing MySQL container: {e}")
        return False

def check_permissions():
    """Check Docker socket permissions"""
    socket_path = '/var/run/docker.sock'
    if os.path.exists(socket_path):
        try:
            # Get file stats
            import stat
            socket_stat = os.stat(socket_path)
            mode = socket_stat.st_mode
            
            # Check if current user can access socket through group permissions
            gid = socket_stat.st_gid
            import grp
            try:
                group_name = grp.getgrgid(gid).gr_name
                print(f"✅ Docker socket group: {group_name} (gid: {gid})")
            except KeyError:
                print(f"⚠️ Docker socket has unknown group ID: {gid}")
            
            # Check user's group membership
            import getpass
            username = getpass.getuser()
            try:
                import pwd
                user_info = pwd.getpwnam(username)
                user_gid = user_info.pw_gid
                
                # Get user's supplementary groups
                import subprocess
                groups_output = subprocess.check_output(['groups', username]).decode('utf-8').strip()
                print(f"👤 Current user: {username}")
                print(f"   Groups: {groups_output}")
                
                # Check if the Docker group is in user's groups
                if group_name in groups_output:
                    print(f"✅ User {username} is in the {group_name} group")
                else:
                    print(f"⚠️ User {username} is NOT in the {group_name} group")
                    print(f"   Recommend: sudo usermod -aG {group_name} {username}")
            except Exception as e:
                print(f"⚠️ Could not check user group membership: {e}")
            
            # Check if socket is readable/writable for group
            if mode & stat.S_IRGRP:
                print("✅ Docker socket has group read permission")
            else:
                print("⚠️ Docker socket does NOT have group read permission")
                
            if mode & stat.S_IWGRP:
                print("✅ Docker socket has group write permission")
            else:
                print("⚠️ Docker socket does NOT have group write permission")
                
            return True
        except Exception as e:
            print(f"❌ Error checking Docker socket permissions: {e}")
            return False
    else:
        print("❌ Docker socket not found at /var/run/docker.sock")
        return False

def check_network():
    """Test for network connectivity to Docker Hub"""
    try:
        import socket
        socket.create_connection(("registry-1.docker.io", 443), timeout=10)
        print("✅ Network connection to Docker Hub available")
        return True
    except Exception as e:
        print(f"⚠️ Network connection to Docker Hub failed: {e}")
        print("   This might affect pulling Docker images")
        return False

def main():
    """Run all checks and tests"""
    print("\n=== Docker Environment Check for SQL Practice Feature ===\n")
    
    # Run checks
    docker_installed = check_docker_installation()
    if not docker_installed:
        print("\n❌ Docker installation check failed. Please install Docker and try again.")
        return False
    
    docker_running = check_docker_running()
    if not docker_running:
        print("\n❌ Docker daemon not running. Please start Docker and try again.")
        return False
    
    check_permissions()
    check_network()
    
    # Only test container if Docker is installed and running
    if docker_installed and docker_running:
        test_mysql_container()
    
    print("\n=== Check Complete ===")
    print("If all checks passed, the SQL Practice feature should work properly.")
    print("If any checks failed, please resolve the issues before using the feature.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
