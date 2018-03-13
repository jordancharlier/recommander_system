angular.module('myApp', [])
            .controller('HomeCtrl', function($scope, $http) {
			
				
			
				$scope.sexeJSON = function(){
				
					$http({
						method: 'POST',
						url: '/getSexeJSON',

					}).then(function(response) {
					    
						$scope.sexeData = response.data;
                                                 
                                          Charts.sexe($scope.sexeData);
					}, function(error) {
						console.log(error);
					});
				}
		                $scope.ageJSON = function(){
					$http({
						method: 'POST',
						url: '/getAgeJSON',

					}).then(function(response) {
						$scope.ageData = response.data;
                                                Charts1.age($scope.ageData);
					}, function(error) {
						console.log(error);
					});
				}
		$scope.recJSON = function(id){
					$http({
						method: 'POST',
						url: '/getRecJSON/'+ id,

					}).then(function(response) {
					    $scope.movies = response.data;
					    console.log("Done");
					}, function(error) {
						console.log(error);
					});
				}
		                $scope.zipJSON = function(){
					$http({
						method: 'POST',
						url: '/getZipJSON',

					}).then(function(response) {
						$scope.zipData = response.data;
                                                Charts2.zip($scope.zipData);
					}, function(error) {
						console.log(error);
					});
				}
		                $scope.occupJSON = function(){
					$http({
						method: 'POST',
						url: '/getOccupJSON',

					}).then(function(response) {
					    $scope.occupData = response.data;
					    Charts3.occup($scope.occupData);
					}, function(error) {
						console.log(error);
					});
				}

                $scope.showHome = true;
		$scope.showGeneralData = false;
		$scope.showRecomandation = false;
		$scope.showMovie = false;
		$scope.id = undefined;

		$scope.home = function(){
		    $scope.showHome = true;
		    $scope.showGeneralData = false;
		    $scope.showRecomandation = false;
		    $scope.showMovie = false;
		}

		$scope.getChartsData = function(){
		    if(!$scope.sexeData){
			$scope.sexeJSON();
			$scope.ageJSON();
			$scope.zipJSON();
			$scope.occupJSON();
		    }
		   
		}

		$scope.showUsersData = function(){
		    $scope.showHome = false;
		    $scope.showGeneralData = true;
		    $scope.showRecomandation = false;
		    $scope.showMovie = false;
		    if($scope.id === undefined){
			x = document.getElementById('inputId');
			$scope.id = x.value;
		    }
		    $scope.getChartsData();
		}
		$scope.getMostViewGenre = function(){
		    $http({
						method: 'POST',
						url: '/getMostViewGenreJSON',

					}).then(function(response) {
					    $scope.MostViewGenreData = response.data;
					    MovieC2.cat($scope.MostViewGenreData);
					}, function(error) {
						console.log(error);
					});
		}
		$scope.getMoviesPerGenre = function(){
		    $http({
						method: 'POST',
						url: '/getMoviesPerGenreJSON',

					}).then(function(response) {
					    $scope.getMoviesPerGenreData = response.data;
					    MovieC.cat($scope.getMoviesPerGenreData);
					}, function(error) {
						console.log(error);
					});
		}

		    
		$scope.getMoviesData = function(){
		    if(!$scope.MostViewGenreData){
		        $scope.getMostViewGenre();
			$scope.getMoviesPerGenre();
		    }
		}
		
		$scope.showMoviesData = function(){
		    $scope.showHome = false;
		    $scope.showGeneralData = false;
		    $scope.showRecomandation = false;
		    $scope.showMovie = true;
		    $scope.getMoviesData();
		}
               
		$scope.recomandation = function(){
		        $scope.showHome = false;
			$scope.showGeneralData = false;
		    $scope.showRecomandation = true;
			$scope.showMovie = false;
			$scope.recJSON(20);
		    
		}

			




		


		

		





               
				
				
				
            })




/////////////////////////
////////////////////////
//////////////////////////////
/////////////////////////////
if(!this.MovieC){
    MovieC = {};
}
(MovieC.cat = function(dataCat){
    if(dataCat){
	
Highcharts.chart('numberCat', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'Percentage of Movies By Categoris'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                style: {
                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                }
            }
        }
    },
    series: [{
        name: 'Percent',
        colorByPoint: true,
        data: dataCat
    }]
});



    }
}
)

if(!this.MovieC2){
    MovieC2 = {};
}
(MovieC2.cat = function(dataCat2){
    if(dataCat2){
	
Highcharts.chart('numberCat2', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie'
    },
    title: {
        text: 'Percentage of view per category'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                style: {
                    color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                }
            }
        }
    },
    series: [{
        name: 'Percent',
        colorByPoint: true,
        data: dataCat2
    }]
});



    }
}
)

if(!this.Charts){
Charts = {};
}
(Charts.sexe = function (sexeData){
if(sexeData){
Highcharts.chart('sexe', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: 0,
        plotShadow: false
    },
    title: {
        text: 'Genders',
        align: 'center',
        verticalAlign: 'middle',
        y: 40
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            dataLabels: {
                enabled: true,
                distance: -50,
                style: {
                    fontWeight: 'bold',
                    color: 'white'
                }
            },
            startAngle: -90,
            endAngle: 90,
            center: ['50%', '75%']
        }
    },
    series: [{
        type: 'pie',
        name: 'percentage',
        innerSize: '50%',
        data: [
            ['MEN',   sexeData.M],
            ['WOMEN',   sexeData.F],
            {
                name: 'Proprietary or Undetectable',
                y: 0.2,
                dataLabels: {
                    enabled: false
                }
            }
        ]
    }]
});
}
else { console.log("");}
});

///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

if(!this.Charts1){
Charts1 = {};
}
(Charts1.age = function (ageData){
if(ageData){
Highcharts.chart('age', {
    chart: {
        type: 'scatter',
        zoomType: 'xy'
    },
    title: {
        text: 'Users ages'
    },
    xAxis: {
        title: {
            enabled: true,
            text: 'age'
        },
        startOnTick: true,
        endOnTick: true,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'totale'
        }
    },
    legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 100,
        y: 70,
        floating: true,
        backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
        borderWidth: 1
    },
    plotOptions: {
        scatter: {
            marker: {
                radius: 5,
                states: {
                    hover: {
                        enabled: true,
                        lineColor: 'rgb(100,100,100)'
                    }
                }
            },
            states: {
                hover: {
                    marker: {
                        enabled: false
                    }
                }
            },
            tooltip: {
                headerFormat: null,
                pointFormat: '{point.x} ans, {point.y} personnes '
            }
        }
    },
    series: [{
        name: 'Ages',
        color: 'rgba(119, 152, 191, .5)',
        data: ageData
    }]
});
}
}
)
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////

// Create the chart
if(!this.Charts3){
Charts3 = {};
}
(Charts3.occup = function (occupData){
    if(occupData){
	console.log(occupData);
Highcharts.chart('occup', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Number of users per Occupation Category'
    },
    xAxis: {
        type: 'category'
    },
    yAxis: {
        title: {
            text: 'Total'
        }

    },
    legend: {
        enabled: false
    },
    plotOptions: {
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y}'
            }
        }
    },

    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b> user(s)<br/>'
    },

    series: [{
        name: 'Number Of',
        colorByPoint: true,
        data: occupData
    }]
});
}
}
)
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////////



if(!this.Charts2){
Charts2 = {};
}
(Charts2.zip = function (zipData){
    if(zipData){
	console.log(zipData[0].categoris);
Highcharts.chart('map', {

    chart: {
        type: 'bubble',
        plotBorderWidth: 1,
        zoomType: 'xy'
    },

    legend: {
        enabled: false
    },

    title: {
        text: 'Number of users'
    },

    subtitle: {
        text: 'per country or state'
    },

    xAxis: {
	categories: zipData[0].categoris
    },

    yAxis: {
        startOnTick: false,
        endOnTick: false,
        title: {
            text: 'Total'
        },
        maxPadding: 0.2,
        plotLines: [{
            color: 'black',
            dashStyle: 'dot',
            width: 2,
            value: 50,
            label: {
                align: 'right',
                style: {
                    fontStyle: 'italic'
                },
                text: 'Safe sugar intake 50g/day',
                x: -10
            },
            zIndex: 3
        }]
    },

    tooltip: {
        useHTML: true,
        headerFormat: '<table>',
        pointFormat: '<tr><th colspan="2"><h3>{point.country}</h3></th></tr>' +
            '<tr><th>State: </th><td>{point.country}</td></tr>' +
            '<tr><th>Total:</th><td>{point.y}</td></tr>' +
            '<tr><th>Zip-Code:</th><td>{point.zip}</td></tr>',
        footerFormat: '</table>',
        followPointer: true
    },

    plotOptions: {
        series: {
            dataLabels: {
                enabled: true,
                format: '{point.name}'
            }
        }
    },

    series: [{
        data: zipData[0].data
    }]

});
}
}
)
