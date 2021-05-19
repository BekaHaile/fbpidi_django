
		$(function () {

			var $subsectorCompanyChart = $("#subsector-company-chart");
		  $.ajax({
			url: $subsectorCompanyChart.data("url"),
			success: function (data) {
	
			  var ctx = $subsectorCompanyChart[0].getContext("2d");
	
			  new Chart(ctx, {
				type: 'bar',
				data: {
				  labels: data.labels,
				  datasets: [{
					label: 'Companies',
					backgroundColor: data.colors,
					data: data.data
				  }]          
				},
				options: {
				  responsive: true,
				  legend: {
					position: 'top',
				  },
				  title: {
					display: true,
					text: 'Number of Industries by Sub Sector'
				  }
				}
			  });
	
			}
		  });
	
		  var $populationChart = $("#certification-chart");
		  $.ajax({
			url: $populationChart.data("url"),
			success: function (data) {
	
			  var ctx = $populationChart[0].getContext("2d");
	
			  new Chart(ctx, {
				type: 'bar',
				data: {
				  labels: data.labels,
				  datasets: [{
					label: 'Companies',
					backgroundColor: data.colors,
					data: data.data
				  }]          
				},
				options: {
				  responsive: true,
				  legend: {
					position: 'top',
				  },
				  title: {
					display: true,
					text: 'Number of Industries by Certification'
				  }
				}
			  });
	
			}
		  });

		  var $mgmtToolChart = $("#tools-chart");
			$.ajax({
			url: $mgmtToolChart.data("url"),
			success: function (data) {

				var ctx = $mgmtToolChart[0].getContext("2d");

				new Chart(ctx, {
				type: 'bar',
				data: {
					labels: data.labels,
					datasets: [{
					label: 'Industries',
					backgroundColor: data.colors,
					data: data.data
					}]          
				},
				options: {
					responsive: true,
					legend: {
					position: 'top',
					},
					title: {
					display: true,
					text: 'Number of Industries by Management Tools'
					}
				}
				});

			}
			});
			// ownership chart
			var $ownershipChart = $("#ownership-chart");
			$.ajax({
			url: $ownershipChart.data("url"),
			success: function (data) {
        console.log(data);
				var ctx = $ownershipChart[0].getContext("2d");

				new Chart(ctx, {
				type: 'bar',
				data: {
					labels: data.labels,
					datasets: [{
					label: 'Industries',
					backgroundColor: data.colors,
					data: data.data
					}]          
				},
				options: {
					responsive: true,
					legend: {
					position: 'top',
					},
					title: {
					display: true,
					text: 'Number of Industries by Form of Ownership'
					}
				}
				});

			}
			});
			// sector data
			var $categoryChart = $("#category-chart");
              $.ajax({
                url: $categoryChart.data("url"),
                success: function (data) {
        
                  var ctx = $categoryChart[0].getContext("2d");
                   
                  new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: 'Industries',
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Company Summary'
                      }
                    }
                  });
        
                }
              });
			//   working hour chart
			var $workinghourChart = $("#working-hour-chart");
              $.ajax({
                url: $workinghourChart.data("url"),
                success: function (data) {
        
                  var ctx = $workinghourChart[0].getContext("2d");
                   
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: 'Industries',
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Companies By Working Hour'
                      }
                    }
                  });
        
                }
              });
			//   investment capital chart
			var $invcapChart = $("#invcap-chart");
              $.ajax({
                url: $invcapChart.data("url"),
                success: function (data) {
        
                  var ctx = $invcapChart[0].getContext("2d");
                   
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: 'Investment Capital',
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Companies Investment Capital'
                      }
                    }
                  });
        
                }
              });
			//production capacity data
			var $pcapChart = $("#pcap-chart");
              $.ajax({
                url: $pcapChart.data("url"),
                success: function (data) {
        
                  var ctx = $pcapChart[0].getContext("2d");
                   
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: 'Production Capacity',
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Products Production Capacity'
                      }
                    }
                  });
        
                }
              });  
			  //Capital Utilization data
			var $capitalutilChart = $("#capital-util-chart");
              $.ajax({
                url: $capitalutilChart.data("url"),
                success: function (data) {
        
                  var ctx = $capitalutilChart[0].getContext("2d");
                   
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: 'Capital Utilization',
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Capital Utilization data'
                      }
                    }
                  });
        
                }
              }); 
			//   change in capital utilization
			var $changecapitalutilChart = $("#change-capital-util-chart");
              $.ajax({
                url: $changecapitalutilChart.data("url"),
                success: function (data) {
        
                  var ctx = $changecapitalutilChart[0].getContext("2d");
                   
                  new Chart(ctx, {
                    type: 'line',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: 'Chnage in Capital Utilization',
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Chnage in Capital Utilization data'
                      }
                    }
                  });
        
                }
              });  
			  // Average Extraction Rate
			var $extnrateChart = $("#extn-rate-chart");
              $.ajax({
                url: $extnrateChart.data("url"),
                success: function (data) {
        
                  var ctx = $extnrateChart[0].getContext("2d");
                   
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: 'Average Extraction Rate',
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Average Extraction Rate of a Product'
                      }
                    }
                  });
        
                }
              }); 
			   // Gross value of production
			var $gvpChart = $("#gvp-chart");
              $.ajax({
                url: $gvpChart.data("url"),
                success: function (data) {
        
                  var ctx = $gvpChart[0].getContext("2d");
                  new Chart(ctx, {
                    type: 'line',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: data.year,
                        backgroundColor: data.colors,
                        data: data.this_year
                      },{
                        label: data.year-1,
                        backgroundColor: data.colors1,
                        data: data.last_year
                      },{
                        label: data.year-2,
                        backgroundColor: data.colors2,
                        data: data.prev_year
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Gross Value of Production'
                      }
                    }
                  });
        
                }
              });
			  //Number of employees
			  var $numempChart = $("#num-emp-chart");
              $.ajax({
                url: $numempChart.data("url"),
                success: function (data) {
        
                  var ctx = $numempChart[0].getContext("2d");
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Employees",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Number of Employees By Sector'
                      }
                    }
                  });
        
                }
              });  
			  //Number of Female employees
			  var $numfemempChart = $("#num-female-emp-chart");
              $.ajax({
                url: $numfemempChart.data("url"),
                success: function (data) {
        
                  var ctx = $numfemempChart[0].getContext("2d");
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Female Employees",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Number of Female Employees By Sector'
                      }
                    }
                  });
        
                }
              });  
			  //Number of Foreign employees
			  var $numforempChart = $("#num-for-emp-chart");
              $.ajax({
                url: $numforempChart.data("url"),
                success: function (data) {
        
                  var ctx = $numforempChart[0].getContext("2d");
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Foreign Employees",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Number of Foreign Employees By Sector'
                      }
                    }
                  });
        
                }
              });  
			  //Number of Female employees
			  var $numjobsChart = $("#num-jobs-chart");
              $.ajax({
                url: $numjobsChart.data("url"),
                success: function (data) {
        
                  var ctx = $numjobsChart[0].getContext("2d");
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Number of Jobs",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Number of Jobs Created By Sector'
                      }
                    }
                  });
        
                }
              });  
			  //Number of Education Level
			  var $numeduChart = $("#num-edu-level-chart");
              $.ajax({
                url: $numeduChart.data("url"),
                success: function (data) {
        
                  var ctx = $numeduChart[0].getContext("2d");
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Male of Employees",
                        backgroundColor: data.colors,
                        data: data.data_male
                      },{
                        label: "Female of Employees",
                        backgroundColor: data.colors,
                        data: data.data_female
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Number of Employees Educational Status By Sector'
                      }
                    }
                  });
        
                }
              }); 
			  //Number of Female Emp in Position Level
			  var $numFemChart = $("#num-fem-chart");
              $.ajax({
                url: $numFemChart.data("url"),
                success: function (data) {
        
                  var ctx = $numFemChart[0].getContext("2d");
                  new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "FeMale Employees",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Number of Female Employees in Position Level'
                      }
                    }
                  });
        
                }
              });  
			  // Available Inputs
			  var $avlinputChart = $("#input-avl-chart");
              $.ajax({
                url: $avlinputChart.data("url"),
                success: function (data) {
        
                  var ctx = $avlinputChart[0].getContext("2d");
                  new Chart(ctx, {
                    type: 'line',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Available Inputs",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Available Inputs'
                      }
                    }
                  });
        
                }
              }); 
			//   local share of inputs
			var $inputshareChart = $("#input-share-chart");
              $.ajax({
                url: $inputshareChart.data("url"),
                success: function (data) {
                   
                  var ctx = $inputshareChart[0].getContext("2d");
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Local Share of Inputs",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Local Share of Inputs'
                      }
                    }
                  });
        
                }
              });  
			//   Energy Source data
			var $esChart = $("#energy-source-chart");
              $.ajax({
                url: $esChart.data("url"),
                success: function (data) {
        
                  var ctx = $esChart[0].getContext("2d");
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Companies",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Number/Share of Companies by Energy Source'
                      }
                    }
                  });
        
                }
              });  
			  //   Market Destination
			var $destinChart = $("#destin-chart");
              $.ajax({
                url: $destinChart.data("url"),
                success: function (data) {
        
                  var ctx = $destinChart[0].getContext("2d");
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Companies",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Number/Share of Companies by Destination'
                      }
                    }
                  });
        
                }
              });  
			  //   Market TARget data
			var $targetChart = $("#target-chart");
              $.ajax({
                url: $targetChart.data("url"),
                success: function (data) {
        
                  var ctx = $targetChart[0].getContext("2d");
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Companies",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Number/Share of Companies by Market Target'
                      }
                    }
                  });
        
                }
              });  
              // Inqury chart by product
              var $inqproductChart = $("#inq-product-chart");
              $.ajax({
                url: $inqproductChart.data("url"),
                success: function (data) {
                  console.log(data);
                  var ctx = $inqproductChart[0].getContext("2d");
                  new Chart(ctx, {
                    type: 'bar',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Inquries",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Product Inqury '
                      }
                    }
                  });
        
                }
              });  

              // Inqury chart by daily
              var $inqdailyChart = $("#inq-daily-chart");
              $.ajax({
                url: $inqdailyChart.data("url"),
                success: function (data) {
                  console.log(data);
                  var ctx = $inqdailyChart[0].getContext("2d");
                  new Chart(ctx, {
                    type: 'line',
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Inquries",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      legend: {
                        position: 'top',
                      },
                      title: {
                        display: true,
                        text: 'Product Inqury Weakly'
                      }
                    }
                  });
        
                }
              });  
	
		});
	
