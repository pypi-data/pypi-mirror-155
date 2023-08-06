import csv
import json
import os
import time
from nose.tools import assert_equal
from nose.tools import assert_true
from nose.tools import assert_false
from nose.tools import assert_raises
from nose.tools import assert_not_equal
from nose.tools import assert_is_not_none
from nose.tools import assert_greater
from boonamber import AmberClient, AmberUserError, AmberCloudError, float_list_to_csv_string
from secrets import get_secrets


# secrets downloaded from points beyond
def create_amber_client():
    amber_license_file = os.environ.get('AMBER_TEST_LICENSE_FILE', None)
    amber_license_id = os.environ.get('AMBER_TEST_LICENSE_ID', None)
    assert_is_not_none(amber_license_id, 'AMBER_TEST_LICENSE_ID is missing in test environment')

    # purge AMBER environment variables
    for key in Test_01_AmberInstance.saved_env.keys():
        if key in os.environ:
            del os.environ[key]

    if amber_license_file is not None:
        # load license profile using a local license file
        amber_client = AmberClient(amber_license_id, amber_license_file)
    else:
        # load license profile from secrets manager
        secret_dict = get_secrets()
        license_profile = secret_dict.get(amber_license_id, None)
        os.environ['AMBER_USERNAME'] = license_profile['username']
        os.environ['AMBER_PASSWORD'] = license_profile['password']
        os.environ['AMBER_SERVER'] = license_profile['server']
        os.environ['AMBER_OAUTH_SERVER'] = license_profile['oauth-server']
        amber_client = AmberClient(None, None)

    return amber_client


class Test_01_AmberInstance:
    # class variable to saved license file name from environment
    saved_env = {
        'AMBER_LICENSE_FILE': None,
        'AMBER_USERNAME': None,
        'AMBER_PASSWORD': None,
        'AMBER_SERVER': None,
        'AMBER_OAUTH_SERVER': None,
        'AMBER_LICENSE_ID': None,
        'AMBER_SSL_CERT': None,
        'AMBER_SSL_VERIFY': None
    }

    @staticmethod
    def clear_environment():
        for key in Test_01_AmberInstance.saved_env:
            if key in os.environ:
                Test_01_AmberInstance.saved_env[key] = os.environ.get(key, None)
                del os.environ[key]

    @staticmethod
    def restore_environment():
        for key, value in Test_01_AmberInstance.saved_env.items():
            if value is not None:
                os.environ[key] = value
            elif key in os.environ:
                del os.environ[key]

    def test_01_init(self):

        Test_01_AmberInstance.clear_environment()

        # load profile using license file specified as parameter
        profile1 = AmberClient(license_file='test.Amber.license')

        # load the same profile using license loaded from environment
        os.environ['AMBER_LICENSE_FILE'] = 'test.Amber.license'
        profile2 = AmberClient()
        assert_equal(profile1.license_profile, profile2.license_profile, 'override with AMBER_LICENSE_FILE')

        # override items in license file through environment
        os.environ['AMBER_USERNAME'] = "xyyyAmberUser"
        os.environ['AMBER_PASSWORD'] = "bogus_password"
        os.environ['AMBER_SERVER'] = "https://temp.amber.boonlogic.com/v1"
        os.environ['AMBER_SSL_CERT'] = "bogus_ssl_cert"
        os.environ['AMBER_SSL_VERIFY'] = "false"
        profile3 = AmberClient(license_file='test.Amber.license')
        assert_equal(profile3.license_profile['server'], "https://temp.amber.boonlogic.com/v1")
        assert_equal(profile3.license_profile['username'], "xyyyAmberUser")
        assert_equal(profile3.license_profile['password'], "bogus_password")
        assert_equal(profile3.license_profile['cert'], "bogus_ssl_cert")
        assert_equal(profile3.license_profile['verify'], False)

        # set configuration through environment with non-existent license file
        os.environ['AMBER_USERNAME'] = "EnvironmentAmberUser"
        os.environ['AMBER_PASSWORD'] = "bogus_password"
        os.environ['AMBER_SERVER'] = "https://temp.amber.boonlogic.com/v1"
        os.environ['AMBER_SSL_CERT'] = "bogus_ssl_cert"
        os.environ['AMBER_SSL_VERIFY'] = "false"
        profile4 = AmberClient(license_file='bogus.Amber.license')
        assert_equal(profile4.license_profile['server'], "https://temp.amber.boonlogic.com/v1")
        assert_equal(profile4.license_profile['username'], "EnvironmentAmberUser")
        assert_equal(profile4.license_profile['password'], "bogus_password")
        assert_equal(profile4.license_profile['cert'], "bogus_ssl_cert")
        assert_equal(profile4.license_profile['verify'], False)

        Test_01_AmberInstance.restore_environment()

    def test_02_init_negative(self):

        Test_01_AmberInstance.clear_environment()

        # no license file specified
        assert_raises(AmberUserError, AmberClient, license_id="default", license_file="nonexistent-license-file")

        # missing required fields
        os.environ['AMBER_LICENSE_FILE'] = "test.Amber.license"
        assert_raises(AmberUserError, AmberClient, license_id="nonexistent-license-id",
                      license_file="test.Amber.license")
        assert_raises(AmberUserError, AmberClient, license_id="missing-username", license_file="test.Amber.license")
        assert_raises(AmberUserError, AmberClient, license_id="missing-password", license_file="test.Amber.license")
        assert_raises(AmberUserError, AmberClient, license_id="missing-server", license_file="test.Amber.license")

        Test_01_AmberInstance.restore_environment()


class Test_02_Authenticate:

    def test_01_authenticate(self):
        amber = create_amber_client()
        print(json.dumps(amber.license_profile, indent=4))
        amber._authenticate()
        assert_not_equal(amber.token, None)
        assert_not_equal(amber.token, '')

    def test_02_authenticate_negative(self):
        amber = create_amber_client()
        # modify the password
        amber.license_profile['password'] = "not-valid"
        with assert_raises(AmberCloudError) as context:
            amber._authenticate()
        assert_equal(context.exception.code, 401)


class Test_03_SensorOps:

    amber = None
    sensor_id = None

    def __init__(self):
        if Test_03_SensorOps.amber is None:
            Test_03_SensorOps.amber = create_amber_client()
            Test_03_SensorOps.sensor_id = Test_03_SensorOps.amber.create_sensor('test-sensor-python')
        self.amber = Test_03_SensorOps.amber
        self.sensor_id = Test_03_SensorOps.sensor_id

    def test_01_create_sensor(self):

        try:
            assert_not_equal(self.sensor_id, None)
            assert_not_equal(self.sensor_id, "")
        except Exception as e:
            raise RuntimeError("setup failed: {}".format(e))

    def test_02_update_label(self):
        label = Test_03_SensorOps.amber.update_label(self.sensor_id, 'new-label')
        assert_equal(label, 'new-label')

        try:
            Test_03_SensorOps.amber.update_label(self.sensor_id, 'test-sensor-python')
        except Exception as e:
            raise RuntimeError("teardown failed, label was not changed back to 'test-sensor-python': {}".format(e))

    def test_03_update_label_negative(self):
        with assert_raises(AmberCloudError) as context:
            label = Test_03_SensorOps.amber.update_label('nonexistent-sensor-id', 'test-sensor-python')
        assert_equal(context.exception.code, 404)

    def test_04_get_sensor(self):
        sensor = Test_03_SensorOps.amber.get_sensor(Test_03_SensorOps.sensor_id)
        assert_equal(sensor['label'], 'test-sensor-python')
        assert_equal(sensor['sensorId'], Test_03_SensorOps.sensor_id)
        assert_true('usageInfo' in sensor)

    def test_05_get_sensor_negative(self):
        with assert_raises(AmberCloudError) as context:
            sensor = Test_03_SensorOps.amber.get_sensor('nonexistent-sensor-id')
        assert_equal(context.exception.code, 404)

    def test_08_list_sensors(self):
        sensors = Test_03_SensorOps.amber.list_sensors()
        assert_true(Test_03_SensorOps.sensor_id in sensors.keys())

    def test_06_configure_sensor(self):
        # configure sensor with custom features
        expected = {
            'featureCount': 1,
            'streamingWindowSize': 25,
            'samplesToBuffer': 1000,
            'anomalyHistoryWindow': 1000,
            'learningRateNumerator': 10,
            'learningRateDenominator': 10000,
            'learningMaxClusters': 1000,
            'learningMaxSamples': 1000000,
            'features': [{
                'minVal': 1,
                'maxVal': 50,
                'label': 'fancy-label',
                'submitRule': 'submit'
            }]
        }
        features = [{
            'minVal': 1,
            'maxVal': 50,
            'label': 'fancy-label'
        }]
        config = Test_03_SensorOps.amber.configure_sensor(Test_03_SensorOps.sensor_id, feature_count=1,
                                                          streaming_window_size=25,
                                                          samples_to_buffer=1000,
                                                          anomaly_history_window=1000,
                                                          learning_rate_numerator=10,
                                                          learning_rate_denominator=10000,
                                                          learning_max_clusters=1000,
                                                          learning_max_samples=1000000,
                                                          features=features)

        assert_equal(config, expected)

        # configure sensor with default features
        expected = {
            'featureCount': 1,
            'streamingWindowSize': 25,
            'samplesToBuffer': 1000,
            'anomalyHistoryWindow': 1000,
            'learningRateNumerator': 10,
            'learningRateDenominator': 10000,
            'learningMaxClusters': 1000,
            'learningMaxSamples': 1000000,
            'features': [{
                'maxVal': 1,
                'minVal': 0,
                'label': 'feature-0',
                'submitRule': 'submit'
            }]
        }
        config = Test_03_SensorOps.amber.configure_sensor(Test_03_SensorOps.sensor_id, feature_count=1,
                                                          streaming_window_size=25,
                                                          samples_to_buffer=1000,
                                                          anomaly_history_window=1000,
                                                          learning_rate_numerator=10,
                                                          learning_rate_denominator=10000,
                                                          learning_max_clusters=1000,
                                                          learning_max_samples=1000000)
        assert_equal(config, expected)

    def test_07_configure_sensor_negative(self):
        with assert_raises(AmberCloudError) as context:
            config = Test_03_SensorOps.amber.configure_sensor('nonexistent-sensor-id')
        assert_equal(context.exception.code, 404)

        # invalid feature_count or streaming_window_size
        assert_raises(AmberUserError, Test_03_SensorOps.amber.configure_sensor, Test_03_SensorOps.sensor_id,
                      feature_count=-1)
        assert_raises(AmberUserError, Test_03_SensorOps.amber.configure_sensor, Test_03_SensorOps.sensor_id,
                      feature_count=1.5)
        assert_raises(AmberUserError, Test_03_SensorOps.amber.configure_sensor, Test_03_SensorOps.sensor_id,
                      streaming_window_size=-1)
        assert_raises(AmberUserError, Test_03_SensorOps.amber.configure_sensor, Test_03_SensorOps.sensor_id,
                      streaming_window_size=1.5)

    def test_08_get_config(self):
        expected = {
            'featureCount': 1,
            'streamingWindowSize': 25,
            'samplesToBuffer': 1000,
            'anomalyHistoryWindow': 1000,
            'learningRateNumerator': 10,
            'learningRateDenominator': 10000,
            'learningMaxClusters': 1000,
            'learningMaxSamples': 1000000,
            'percentVariation': 0.05,
            'features': [{'minVal': 0, 'maxVal': 1, 'label': 'feature-0', 'submitRule': 'submit'}]
        }
        config = Test_03_SensorOps.amber.get_config(Test_03_SensorOps.sensor_id)
        assert_equal(config, expected)

    def test_09_get_config_negative(self):
        with assert_raises(AmberCloudError) as context:
            config = Test_03_SensorOps.amber.get_config('nonexistent-sensor-id')
        assert_equal(context.exception.code, 404)

    def test_10_configure_fusion(self):
        # fusion tests setup
        Test_03_SensorOps.amber.configure_sensor(Test_03_SensorOps.sensor_id, feature_count=5, streaming_window_size=1)

        f = [{'label': 'f{}'.format(i), 'submitRule': 'submit'} for i in range(5)]
        resp = Test_03_SensorOps.amber.configure_fusion(Test_03_SensorOps.sensor_id, features=f)
        assert_equal(resp, f)

    def test_11_configure_fusion_negative(self):
        f = [{'label': 'f{}'.format(i), 'submitRule': 'submit'} for i in range(5)]

        # missing sensor
        with assert_raises(AmberCloudError) as context:
            Test_03_SensorOps.amber.configure_fusion('nonexistent-sensor-id', features=f)
        assert_equal(context.exception.code, 404)

        # number of features doesn't match configured feature_count
        with assert_raises(AmberCloudError) as context:
            Test_03_SensorOps.amber.configure_fusion(Test_03_SensorOps.sensor_id, features=f[:4])
        assert_equal(context.exception.code, 400)

        # duplicate feature in configuration
        badf = f.copy()
        badf[3] = badf[2]
        with assert_raises(AmberCloudError) as context:
            Test_03_SensorOps.amber.configure_fusion(Test_03_SensorOps.sensor_id, features=badf)
        assert_equal(context.exception.code, 400)

        # unrecognized submit rule in configuration
        badf = f.copy()
        badf[2]['submitRule'] = 'badsubmitrule'
        with assert_raises(AmberCloudError) as context:
            Test_03_SensorOps.amber.configure_fusion(Test_03_SensorOps.sensor_id, features=badf)
        assert_equal(context.exception.code, 400)

    def test_12_stream_fusion(self):
        # stream partial vector (204 response)
        v = [{'label': 'f1', 'value': 2}, {'label': 'f3', 'value': 4}]
        exp = {'vector': "None,2,None,4,None"}
        resp = Test_03_SensorOps.amber.stream_fusion(Test_03_SensorOps.sensor_id, vector=v)
        assert_equal(resp, exp)

        # stream full vector (200 response)
        v = [{'label': 'f0', 'value': 1}, {'label': 'f2', 'value': 3}, {'label': 'f4', 'value': 5}]
        exp = {
            'vector': "1,2,3,4,5",
            'results': {
                'clusterCount': 0,
                'message': '',
                'progress': 0,
                'retryCount': 0,
                'state': "Buffering",
                'streamingWindowSize': 1,
                'totalInferences': 0,
                'AD': [0], 'AH': [0], 'AM': [0], 'AW': [0], 'ID': [0], 'RI': [0], 'SI': [0]
            }
        }
        resp = Test_03_SensorOps.amber.stream_fusion(Test_03_SensorOps.sensor_id, vector=v)
        assert_equal(resp, exp)

    def test_13_stream_fusion_negative(self):
        # fusion vector contains label not in fusion configuration
        v = [{'label': 'badfeature', 'value': 2}, {'label': 'f3', 'value': 4}]
        with assert_raises(AmberCloudError) as context:
            Test_03_SensorOps.amber.stream_fusion(Test_03_SensorOps.sensor_id, vector=v)
        assert_equal(context.exception.code, 400)

        # fusion vector contains duplicate label
        v = [{'label': 'f3', 'value': 2}, {'label': 'f3', 'value': 4}]
        with assert_raises(AmberCloudError) as context:
            Test_03_SensorOps.amber.stream_fusion(Test_03_SensorOps.sensor_id, vector=v)
        assert_equal(context.exception.code, 400)

        # fusion tests teardown
        Test_03_SensorOps.amber.configure_sensor(Test_03_SensorOps.sensor_id, feature_count=1,
                                                 streaming_window_size=25)  # teardown

    def test_14_stream_sensor(self):
        results = Test_03_SensorOps.amber.stream_sensor(Test_03_SensorOps.sensor_id, 1)
        assert_true('state' in results)
        assert_true('message' in results)
        assert_true('progress' in results)
        assert_true('clusterCount' in results)
        assert_true('retryCount' in results)
        assert_true('streamingWindowSize' in results)
        assert_true('SI' in results)
        assert_true('AD' in results)
        assert_true('AH' in results)
        assert_true('AM' in results)
        assert_true('AW' in results)

        # scalar data should return SI of length 1
        assert_true(len(results['SI']) == 1)

        # array data should return SI of same length
        results = Test_03_SensorOps.amber.stream_sensor(Test_03_SensorOps.sensor_id, [1, 2, 3, 4, 5])
        assert_true(len(results['SI']) == 5)

    def test_15_stream_sensor_negative(self):
        with assert_raises(AmberCloudError) as context:
            results = Test_03_SensorOps.amber.stream_sensor('nonexistent-sensor-id', [1, 2, 3, 4, 5])
        assert_equal(context.exception.code, 404)

        # invalid data
        assert_raises(AmberUserError, Test_03_SensorOps.amber.stream_sensor, Test_03_SensorOps.sensor_id, [])
        assert_raises(AmberUserError, Test_03_SensorOps.amber.stream_sensor, Test_03_SensorOps.sensor_id, [1, '2', 3])
        assert_raises(AmberUserError, Test_03_SensorOps.amber.stream_sensor, Test_03_SensorOps.sensor_id,
                      [1, [2, 3], 4])

    def test_16_post_outage(self):
        results = Test_03_SensorOps.amber.post_outage(Test_03_SensorOps.sensor_id)
        assert_equal("Buffering", results["state"])

        results = Test_03_SensorOps.amber.stream_sensor(Test_03_SensorOps.sensor_id, [1, 2, 3, 4, 5])
        assert_true(list(set(results['ID'])) == [0])

    def test_17_post_outage_negative(self):
        with assert_raises(AmberCloudError) as context:
            results = Test_03_SensorOps.amber.post_outage('nonexistent-sensor-id')
        assert_equal(context.exception.code, 404)

    def test_18_get_root_cause(self):
        config = Test_03_SensorOps.amber.get_config(Test_03_SensorOps.sensor_id)
        expected = [[0] * len(config['features']) * config['streamingWindowSize']] * 2
        config = Test_03_SensorOps.amber.get_root_cause(Test_03_SensorOps.sensor_id,
                                                        pattern_list=[
                                                            [1] * len(config['features']) * config[
                                                                'streamingWindowSize'],
                                                            [0] * len(config['features']) * config[
                                                                'streamingWindowSize']])
        assert_equal(config, expected)

    def test_19_get_root_cause_negative(self):
        with assert_raises(AmberCloudError) as context:
            config = Test_03_SensorOps.amber.get_root_cause('nonexistent-sensor-id', id_list=[1])
        assert_equal(context.exception.code, 404)

        # give both fail
        with assert_raises(AmberUserError) as context:
            config = Test_03_SensorOps.amber.get_root_cause(Test_03_SensorOps.sensor_id, id_list=[1],
                                                            pattern_list=[[1, 2, 3], [4, 5, 6]])

        # give neither fail
        with assert_raises(AmberUserError) as context:
            config = Test_03_SensorOps.amber.get_root_cause(Test_03_SensorOps.sensor_id)

        assert_raises(AmberCloudError, Test_03_SensorOps.amber.get_root_cause, Test_03_SensorOps.sensor_id, [1])

    def test_20_get_status(self):
        status = Test_03_SensorOps.amber.get_status(Test_03_SensorOps.sensor_id)
        assert_true('pca' in status)
        assert_true('numClusters' in status)

    def test_21_get_status_negative(self):
        with assert_raises(AmberCloudError) as context:
            status = Test_03_SensorOps.amber.get_status('nonexistent-sensor-id')
        assert_equal(context.exception.code, 404)

    def test_22_get_pretrain_state(self):
        response = Test_03_SensorOps.amber.get_pretrain_state(Test_03_SensorOps.sensor_id)
        assert_true('state' in response)
        assert_equal(response['state'], 'None')

    def test_23_get_pretrain_state_negative(self):
        with assert_raises(AmberCloudError) as context:
            response = Test_03_SensorOps.amber.get_pretrain_state('nonexistent-sensor-id')
        assert_equal(context.exception.code, 404)

    def test_24_pretrain_sensor(self):
        with open('output_current.csv', 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            data = []
            for row in csv_reader:
                for d in row:
                    data.append(float(d))

        results = Test_03_SensorOps.amber.pretrain_sensor(Test_03_SensorOps.sensor_id, data, block=True)
        assert_equal(results['state'], 'Pretrained')

        results = Test_03_SensorOps.amber.pretrain_sensor(Test_03_SensorOps.sensor_id, data, block=False)
        assert_true('Pretraining' in results['state'] or 'Pretrained' in results['state'])
        while True:
            time.sleep(5)
            results = Test_03_SensorOps.amber.get_pretrain_state(Test_03_SensorOps.sensor_id)
            if results['state'] == 'Pretraining':
                continue
            else:
                break
        assert_equal(results['state'], 'Pretrained')

    def test_25_pretrain_sensor_negative(self):
        with assert_raises(AmberCloudError) as context:
            response = Test_03_SensorOps.amber.pretrain_sensor('123456abcdef', [1, 2, 3, 4, 5], block=True)
        assert_equal(context.exception.code, 404)

        # not enough data to fill sample buffer
        with assert_raises(AmberCloudError) as context:
            response = Test_03_SensorOps.amber.pretrain_sensor(Test_03_SensorOps.sensor_id, [1, 2, 3, 4, 5], block=True)
        assert_equal(context.exception.code, 400)

    def test_26_enable_learning(self):
        # enable learning tests setup
        exp = {
                "anomalyHistoryWindow": 1000,
                "learningRateNumerator": 10,
                "learningRateDenominator": 10000,
                "learningMaxClusters": 1000,
                "learningMaxSamples": 1000000
              }
        resp = Test_03_SensorOps.amber.enable_learning(Test_03_SensorOps.sensor_id, anomaly_history_window=1000,
                                                       learning_rate_numerator=10,
                                                       learning_rate_denominator=10000,
                                                       learning_max_clusters=1000,
                                                       learning_max_samples=1000000)
        assert_equal(resp, exp)

    def test_27_enable_learning_negative(self):
        exp = {"streaming": {
                "anomalyHistoryWindow": 1000,
                "learningRateNumerator": 10,
                "learningRateDenominator": 10000,
                "learningMaxClusters": 1000,
                "learningMaxSamples": 1000000}
              }
        # missing sensor
        with assert_raises(AmberCloudError) as context:
            Test_03_SensorOps.amber.enable_learning('nonexistent-sensor-id', learning_max_samples=1000000)
        assert_equal(context.exception.code, 404)

        with assert_raises(AmberCloudError) as context:
            Test_03_SensorOps.amber.enable_learning(Test_03_SensorOps.sensor_id, learning_max_samples=-1)
        assert_equal(context.exception.code, 400)

        # not in learning state
        Test_03_SensorOps.amber.configure_sensor(Test_03_SensorOps.sensor_id, feature_count=5, streaming_window_size=1)
        with assert_raises(AmberCloudError) as context:
            Test_03_SensorOps.amber.enable_learning(Test_03_SensorOps.sensor_id, learning_max_samples=1000000)
        assert_equal(context.exception.code, 400)

    def test_28_delete_sensor_negative(self):
        with assert_raises(AmberCloudError) as context:
            Test_03_SensorOps.amber.delete_sensor('nonexistent-sensor-id')
        assert_equal(context.exception.code, 404)

    def test_29_delete_sensor(self):
        try:
            Test_03_SensorOps.amber.delete_sensor(Test_03_SensorOps.sensor_id)
        except Exception as e:
            raise RuntimeError("teardown failed, sensor was not deleted: {}".format(e))


class Test_04_ApiReauth:

    def test_api_reauth(self):
        # create amber instance and mark auth_time
        amber = create_amber_client()
        saved_reauth_time = amber.reauth_time

        # first call covers reauth case, reauth time should be set bigger than initial time
        _ = amber.list_sensors()
        assert_greater(amber.reauth_time, saved_reauth_time)
        saved_reauth_time = amber.reauth_time

        _ = amber.list_sensors()
        # The reauth time should not have changed
        assert_equal(amber.reauth_time, saved_reauth_time)

        # Add 60 to the reauth_time and reissue api call, reauth should occur
        amber.reauth_time += 61
        _ = amber.list_sensors()
        assert_greater(amber.reauth_time, saved_reauth_time)


class Test_04_CSVConvert:

    def test_convert_to_csv(self):
        amber = create_amber_client()

        # valid scalar inputs
        assert_equal("1.0", float_list_to_csv_string(1))
        assert_equal("1.0", float_list_to_csv_string(1.0))

        # valid 1d inputs
        assert_equal("1.0,2.0,3.0", float_list_to_csv_string([1, 2, 3]))
        assert_equal("1.0,2.0,3.0", float_list_to_csv_string([1, 2, 3.0]))
        assert_equal("1.0,2.0,3.0", float_list_to_csv_string([1.0, 2.0, 3.0]))

        # valid 2d inputs
        assert_equal("1.0,2.0,3.0,4.0", float_list_to_csv_string([[1, 2], [3, 4]]))
        assert_equal("1.0,2.0,3.0,4.0", float_list_to_csv_string([[1, 2, 3, 4]]))
        assert_equal("1.0,2.0,3.0,4.0", float_list_to_csv_string([[1], [2], [3], [4]]))
        assert_equal("1.0,2.0,3.0,4.0", float_list_to_csv_string([[1, 2], [3, 4.0]]))
        assert_equal("1.0,2.0,3.0,4.0", float_list_to_csv_string([[1.0, 2.0], [3.0, 4.0]]))

    def test_convert_to_csv_negative(self):
        amber = create_amber_client()

        # empty data
        assert_raises(ValueError, float_list_to_csv_string, [])
        assert_raises(ValueError, float_list_to_csv_string, [[]])
        assert_raises(ValueError, float_list_to_csv_string, [[], []])

        # non-numeric data
        assert_raises(ValueError, float_list_to_csv_string, None)
        assert_raises(ValueError, float_list_to_csv_string, 'a')
        assert_raises(ValueError, float_list_to_csv_string, 'abc')
        assert_raises(ValueError, float_list_to_csv_string, [1, None, 3])
        assert_raises(ValueError, float_list_to_csv_string, [1, 'a', 3])
        assert_raises(ValueError, float_list_to_csv_string, [1, 'abc', 3])
        assert_raises(ValueError, float_list_to_csv_string, [[1, None], [3, 4]])
        assert_raises(ValueError, float_list_to_csv_string, [[1, 'a'], [3, 4]])
        assert_raises(ValueError, float_list_to_csv_string, [[1, 'abc'], [3, 4]])

        # badly-shaped data
        assert_raises(ValueError, float_list_to_csv_string, [1, [2, 3], 4])  # mixed nesting
        assert_raises(ValueError, float_list_to_csv_string, [[1, 2], [3, 4, 5]])  # ragged array
        assert_raises(ValueError, float_list_to_csv_string, [[[1, 2, 3, 4]]])  # nested too deep
        assert_raises(ValueError, float_list_to_csv_string, [[[1], [2], [3], [4]]])


class Test_05_Version:

    def test_01_version(self):
        amber = create_amber_client()
        version = amber.get_version()
        assert_equal(7, len(version.keys()))
        assert_true('api-version' in version.keys())
        assert_true('builder' in version.keys())
        assert_true('expert-api' in version.keys())
        assert_true('expert-common' in version.keys())
        assert_true('nano-secure' in version.keys())
        assert_true('release' in version.keys())
        assert_true('swagger-ui' in version.keys())
        assert_false('rXelXeXaseX' in version.keys())
