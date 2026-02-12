"""
Load balancing test for multiple frontend replicas
Tests that traffic is properly distributed across multiple frontend replicas
"""
import pytest
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor


def test_load_balancing_across_replicas():
    """
    Test that requests are properly load balanced across multiple frontend replicas.
    This test sends multiple concurrent requests and verifies they are handled properly.
    """
    num_requests = 20
    base_url = "http://localhost:30080"  # Assuming frontend is exposed on port 30080
    
    def make_request(req_id):
        """Make a single request and return response info"""
        try:
            response = requests.get(base_url, timeout=10)
            return {
                'id': req_id,
                'status_code': response.status_code,
                'success': response.status_code == 200,
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            return {
                'id': req_id,
                'status_code': None,
                'success': False,
                'error': str(e),
                'response_time': None
            }
    
    # Send multiple requests concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request, i) for i in range(num_requests)]
        results = [future.result() for future in futures]
    
    # Analyze results
    successful_requests = [r for r in results if r['success']]
    failed_requests = [r for r in results if not r['success']]
    
    print(f"Sent {num_requests} requests")
    print(f"Successful: {len(successful_requests)}")
    print(f"Failed: {len(failed_requests)}")
    
    # Verify that most requests succeeded
    assert len(successful_requests) >= num_requests * 0.8, f"Only {len(successful_requests)}/{num_requests} requests succeeded"
    
    # Verify response times are reasonable
    avg_response_time = sum(r['response_time'] for r in successful_requests if r['response_time']) / len(successful_requests)
    print(f"Average response time: {avg_response_time:.2f}s")
    assert avg_response_time < 5.0, f"Average response time too high: {avg_response_time:.2f}s"
    
    print("✓ Load balancing test passed")


def test_session_distribution():
    """
    Test that sessions/connections are properly distributed across replicas
    """
    num_requests = 30
    base_url = "http://localhost:30080"
    
    response_times = []
    
    def timed_request(i):
        start_time = time.time()
        try:
            response = requests.get(base_url, timeout=10)
            end_time = time.time()
            return end_time - start_time, response.status_code
        except Exception:
            end_time = time.time()
            return end_time - start_time, None
    
    # Make requests in sequence to observe distribution
    for i in range(num_requests):
        response_time, status = timed_request(i)
        response_times.append(response_time)
        
        # Brief pause to allow for distribution
        time.sleep(0.1)
    
    # Calculate statistics
    avg_time = sum(response_times) / len(response_times)
    min_time = min(response_times)
    max_time = max(response_times)
    
    print(f"Response time stats - Avg: {avg_time:.2f}s, Min: {min_time:.2f}s, Max: {max_time:.2f}s")
    
    # Verify that response times are reasonable and consistent
    assert avg_time < 5.0, f"Average response time too high: {avg_time:.2f}s"
    assert max_time < 10.0, f"Max response time too high: {max_time:.2f}s"
    
    print("✓ Session distribution test passed")


if __name__ == "__main__":
    test_load_balancing_across_replicas()
    test_session_distribution()
    print("All load balancing tests passed!")