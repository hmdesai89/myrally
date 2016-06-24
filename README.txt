users :
    [ { access_key : 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx' ,
      secret_key : "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' },
     { access_key : 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy' ,
       secret_key : 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy' },
    ]

test_suites :
    [ ##{ test_case : [myrally.test.concurrent_test.ConcurrentVPCTest.test_vpc_create_delete,],
      #  limit : 5,
      #  iterations : 100 },
     # { test_case : [myrally.test.concurrent_test.ConcurrentVPCTest.test_describe_vpcs_resp],
      #  limit : 15, 
      #  iterations : 1000       
      #},
      { test_case : [myrally.test.concurrent_test.DescriberTest.test_describe_subnet_resp],
        limit : 1,
        iterations : 1
      },
      { test_case : [myrally.test.concurrent_test.ConcurrentSubnetTest.test_subnet_create_delete],
        limit : 2,
        iterations : 2
      },



    ]

runner:
    type : parallel
    iteration_per_test : 100
    request_at_a_time : 10
environment :
    vpc_url : 'https://network.jiocloud.com'
    compute_url: 'http://127.0.0.1:8788' 



