
		$(function () {

      Chart.register(ChartDataLabels);
      Chart.defaults.set('plugins.datalabels', {
       color:'black',
       anchor:'end',
            align:'top',
      });
      // if(chart_type == 'bar'){
      //     Chart.defaults.set('plugins.datalabels', {
      //       anchor:'end',
      //       align:'top',
      //     });
      //   }else if(chart_type == "pie"){
      //   Chart.defaults.set('plugins.datalabels', {
      //     color:'white',
      //     anchor:'start',
      //     align:'center',
      //   });
      // }
			var $subsectorCompanyChart = $("#subsector-company-chart");
		  $.ajax({
			url: $subsectorCompanyChart.data("url"),
			success: function (data) {
	
			  var ctx = $subsectorCompanyChart[0].getContext("2d");
	
			  subsectorCompanyChart = new Chart(ctx, {
				type: chart_type,
				data: {
				  labels: data.labels,
				  datasets: [{
					label: 'Number of Companies By Sub Sector',
					backgroundColor: data.colors,
					data: data.data,
          
				  }]          
				},
				options: {
				  responsive: true,
				  plugins:{
            title: {
              display: true,
              text: 'Number of Industries by Sub Sector'
              },
              legend: {
                position: 'top',
                }
            }
            
          }
			  });
	
			}
		  });
	
		  var $certificationChart = $("#certification-chart");
		  $.ajax({
			url: $certificationChart.data("url"),
			success: function (data) {
        if(chart_type == ""){
          chart_type = data.chart_type;
        }
			  var ctx = $certificationChart[0].getContext("2d");
        
			  certificationChart = new Chart(ctx, {
        type: chart_type,
				data: {
				  labels: data.labels,
				  datasets: [{
					label: 'Number of Industries By Certification',
					backgroundColor: data.colors,
					data: data.data
				  }]          
				},
        options: {
				  responsive: true,
				  plugins:{
            legend: {
              position: 'top',
              },
            title: {
              display: true,
              text: 'Number of Industries by Certification'
              }
    
          },
				}
			  });
	
			}
		  });

		  var $mgmtToolChart = $("#tools-chart");
			$.ajax({
			url: $mgmtToolChart.data("url"),
			success: function (data) {
       
				var ctx = $mgmtToolChart[0].getContext("2d");

				mgmtToolChart = new Chart(ctx, {
				type: chart_type,
				data: {
					labels: data.labels,
					datasets: [{
					label: 'Number of Industries by Management Tools',
					backgroundColor: data.colors,
					data: data.data
					}]          
				},
				options: {
					responsive: true,
					plugins:{
            legend: {
              position: 'top',
              },
              title: {
              display: true,
              text: 'Number of Industries by Management Tools'
              }
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

				onwershipChart = new Chart(ctx, {
				type: chart_type,
				data: {
					labels: data.labels,
					datasets: [{
					label: 'Number of Industries by Form of Ownership',
					backgroundColor: data.colors,
					data: data.data
					}]          
				},
				options: {
					responsive: true,
					plugins:{
            legend: {
              position: 'top',
              },
              title: {
              display: true,
              text: 'Number of Industries by Form of Ownership'
              }
          },
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
                   
                  categoryChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: 'Number of Industries By Sector',
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Number of Industries By Sector'
                        }
                      },
                      
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
                   
                  workinghourChart = new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: 'Number of Industries by Working hour',
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Companies By Working Hour'
                        }
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
                   
                  invcapChart = new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: 'Industries Investment Capital',
                        backgroundColor: data.colors,
                        data: data.data,
                        datalabels:{
                        anchor:'end',
                          align:'right',
                        },
                      }]          
                    },
                    plugins:[ChartDataLabels],
                    options: {
                     
                      indexAxis: 'y',
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Companies Investment Capital'
                        }
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
                   
                  pcapChart= new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: 'Industries Production Capacity',
                        backgroundColor: data.colors,
                        data: data.data,
                        datalabels:{
                          anchor:'end',
                            align:'right',
                          },
                      }]          
                    },
                    options: {
                      indexAxis: 'y',
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Products Production Capacity'
                        }
                      }
                    }
                  });
        
                }
              });  
			  //Capacity Utilization data
			var $capitalutilChart = $("#capital-util-chart");
              $.ajax({
                url: $capitalutilChart.data("url"),
                success: function (data) {
        
                  var ctx = $capitalutilChart[0].getContext("2d");
                   
                  capitalutilChart= new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: 'Industries Capacity Utilization',
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Capacity Utilization data'
                        }
                      }
                    }
                  });
        
                }
              }); 
			//   change in capacity utilization
			var $changecapitalutilChart = $("#change-capital-util-chart");
              $.ajax({
                url: $changecapitalutilChart.data("url"),
                success: function (data) {
        
                  var ctx = $changecapitalutilChart[0].getContext("2d");
                   
                  changecapitalutilChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: 'Change in Capacity Utilization',
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Change in Capacity Utilization data'
                        }
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
                   
                  extnrateChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: 'Average Extraction Rate',
                        backgroundColor: data.colors,
                        data: data.data,
                        datalabels:{
                          anchor:'end',
                            align:'right',
                          },
                      }]          
                    },
                    options: {
                      indexAxis: 'y',
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Average Extraction Rate of a Product'
                        }
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
                  gvpChart =    new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: data.year,
                        backgroundColor: ['#32e36a'],
                        data: data.this_year,
                        datalabels:{
                          anchor:'end',
                            align:'right',
                          }, 
                      },{
                        label: data.year-1,
                        backgroundColor: ['#1b73d1'],
                        data: data.last_year,
                        datalabels:{
                          anchor:'end',
                            align:'right',
                          },
                           
                      },{
                        label: data.year-2,
                        backgroundColor: ['#ad1856'],
                        data: data.prev_year,
                        datalabels:{
                          anchor:'end',
                            align:'right',
                          },
                         
                      },
                      
                    ]          
                    },
                    options: {
                      
                      indexAxis: 'y',
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                          
                        },
                        title: {
                          display: true,
                          text: 'Gross Value of Production'
                        }
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
                  numempChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Number of Employees by Sector",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                          
                        },
                        title: {
                          display: true,
                          text: 'Number of Employees By Sector'
                        }
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
                  numfemempChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Number of Female Employees By Sector",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Number of Female Employees By Sector'
                        }
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
                  numforempChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Number of Foreign Employees by Sector",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Number of Foreign Employees By Sector'
                        }
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
                  numjobsChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Number of Jobs Created By Sector",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'bottom',
                        },
                        title: {
                          display: true,
                          text: 'Number of Jobs Created By Sector'
                        }
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
                  numeduChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Male Employees",
                        backgroundColor: data.colors,
                        data: data.data_male
                      },{
                        label: "Female Employees",
                        backgroundColor: data.colors,
                        data: data.data_female
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Number of Employees Educational Status By Sector'
                        }
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
                  numFemChart =  new Chart(ctx, {
                    type: chart_type,
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
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Number of Female Employees in Position Level'
                        }
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
                  avlinputChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Available Inputs",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      indexAxis:'y',
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Available Inputs'
                        }
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
                  inputshareChart =    new Chart(ctx, {
                    type: chart_type,
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
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Local Share of Inputs'
                        }
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
                  esChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Number of Industries by Energy Source",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Number/Share of Companies by Energy Source'
                        }
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
                  destinChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Number of Industries By Market Destination",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Number/Share of Companies by Destination'
                        }
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
                  targetChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Number of Industries By Market Target",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Number/Share of Companies by Market Target'
                        }
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
                    type: chart_type,
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
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Product Inqury '
                        }
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
                    type: chart_type,
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
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Product Inqury Weakly'
                        }
                      }
                    }
                  });
        
                }
              });  
              
              // company-product-group-chart
              var $companyPGChart = $("#company-product-grp");
              $.ajax({
                url: $companyPGChart.data("url"),
                success: function (data) {
                  console.log(data);
                  var ctx = $companyPGChart[0].getContext("2d");
                  companyPGChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Number of Industries By Product Group",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Companies By Product Group'
                        }
                      }
                    }
                  });
        
                }
              }); 
              // Company-therapy-group
              var $companyTGChart = $("#company-terapy-grp");
              $.ajax({
                url: $companyTGChart.data("url"),
                success: function (data) {
                  console.log(data);
                  var ctx = $companyTGChart[0].getContext("2d");
                  companyTGChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Number of Industries By Therapeutic Group",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Companies By therapeutic Group'
                        }
                      }
                    }
                  });
        
                }
              }); 
              // company-dosage-form
              var $companyDFChart = $("#company-dosage-form");
              $.ajax({
                url: $companyDFChart.data("url"),
                success: function (data) {
                  console.log(data);
                  var ctx = $companyDFChart[0].getContext("2d");
                  companyDFChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Number of Industries By Dosage Form",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Companies By Dosage Form'
                        }
                      }
                    }
                  });
        
                }
              }); 
              // product-product-group
              var $productPGChart = $("#product-product-grp");
              $.ajax({
                url: $productPGChart.data("url"),
                success: function (data) {
                  console.log(data);
                  var ctx = $productPGChart[0].getContext("2d");
                  productPGChart =  new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Number of Products by Product group",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Products By Product Group'
                        }
                      }
                    }
                  });
        
                }
              }); 
              // product therapy group
              var $productTGChart = $("#product-terapy-grp");
              $.ajax({
                url: $productTGChart.data("url"),
                success: function (data) {
                  var ctx = $productTGChart[0].getContext("2d");
                  productTGChart =   new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Number of Products therapeutic Group",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Products By Therapeutic Group'
                        }
                      }
                    }
                  });
        
                }
              }); 
              // product-dosage-form
              var $productDFChart = $("#product-dosage-form");
              $.ajax({
                url: $productDFChart.data("url"),
                success: function (data) {
                  var ctx = $productDFChart[0].getContext("2d");
                  productDFChart = new Chart(ctx, {
                    type: chart_type,
                    data: {
                      labels: data.labels,
                      datasets: [{
                        label: "Number of Products by Dosage Form",
                        backgroundColor: data.colors,
                        data: data.data
                      }]          
                    },
                    options: {
                      responsive: true,
                      plugins:{
                        legend: {
                          position: 'top',
                        },
                        title: {
                          display: true,
                          text: 'Products By Dosage Form'
                        }
                      }
                    }
                  });
        
                }
              }); 
            
		});
	
