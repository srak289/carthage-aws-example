from carthage import *
import carthage
from carthage.config import ConfigLayout
from carthage.dependency_injection import *
from carthage.modeling import *
from carthage.machine import BaseCustomization
from carthage.network import V4Config

from carthage_base import *
from carthage_aws.network import *
from carthage_aws.vm import *
from carthage_aws.dns import *

class layout(CarthageLayout, AnsibleModelMixin):

    add_provider(machine_implementation_key, dependency_quote(AwsVm))

    domain = "test.photon.ac"

    @provides('test-subnet')
    class test_subnet(NetworkModel):
        name = "test-subnet"
        v4_config = V4Config(
            network = "192.168.101.0/24"
        )

    add_provider(InjectionKey(AwsHostedZone), when_needed(AwsHostedZone, name="test.photon.ac"))

    @inject(zone=InjectionKey(AwsHostedZone), model=AbstractMachineModel)
    class make_a_record(ModelTasks, AsyncInjectable):
        async def async_ready(self):
            #await self.zone.update_record(self.model.name, self.model.machine.ip_address, 'A')
            # Non async dependency injected into async context
            await self.zone.update_record('carthage_test.test.photon.ac', '192.168.101.5', 'A')
            return await super().async_ready()

    class test_vm(MachineModel):

        name = 'carthage_test'
        key = 'carthage-key'
        imageid = "ami-06ed7917b75fcaf17"
        # buster
        # imageid = "ami-089fe97bc00bff7cc"
        size = "t2.micro"

        ip_address = '192.168.101.5'
        fqdn = f'{name}.{domain}'

        class netconfig(NetworkConfigModel):
            add('eth0', mac='None', net=injector_access('test-subnet'),
                v4_config=V4Config(
                    dhcp=False,
                    address=ip_address,
                    network='192.168.101.0/24'
                )
            )
