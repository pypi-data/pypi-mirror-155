from .handy_mix import HandyMix


class EnvVariables:
    """ Generate the environmental variables to be used by kubernetes """

    @staticmethod
    def generate_env_file(yaml_path='./environments/prd1/step01.yaml', env_path='./.env'):
        """ Save the data from the yaml file into a .env file to be used by decouple
        :param yaml_path: Path to Yaml file
        :param env_path: Path to destination file
        """
        # Read lines from .env file
        f = open(yaml_path, 'r')
        text_content = f.readlines()
        f.close()

        # Find starting index for env variables
        text_content = [str(elem).strip() for elem in text_content]
        first_ind = text_content.index('env:') + 1

        # Find last index for env variables
        boolean_list = ['value' in str(elem) for elem in text_content[::-1]]
        last_ind = len(text_content) - boolean_list.index(True)

        # Get the final variables set
        final_set = text_content[first_ind:last_ind]

        # Prepare .env file structure
        values_pairs = []
        for index in range(int(len(final_set) / 2)):
            value_pair_str = str(final_set[2 * index]).replace(" ", "").replace("-name:", "")
            value_pair_str += "="
            value_pair_str += str(final_set[2 * index + 1]).replace(" ", "").replace("value:", "").replace('"', "")

            values_pairs.append(value_pair_str)

        # Write value pairs to .env file
        f = open(env_path, "w")
        f.write('\n'.join(values_pairs))
        f.close()

    @staticmethod
    def generate_yaml_file(yaml_path='./environments/prd1/step01.yaml', env_path='./.env'):
        """ Save the data from the .env file into a yaml file to be used by kubernetes
        :param yaml_path: Path to Yaml file
        :param env_path: Path to destination file
        """
        # Read lines from yaml file
        f = open(yaml_path, 'r')
        yaml_content = f.readlines()
        f.close()

        # Read yaml content
        yaml_content_mod = [str(elem).strip() for elem in yaml_content]
        break_ind = yaml_content_mod.index('containers:')

        # Find the index where the env variables are to be inserted
        insert_ind = 0
        leading_spaces = len(yaml_content[break_ind]) - len(yaml_content[break_ind].lstrip())
        for ind in range(break_ind + 2, len(yaml_content)):
            if len(yaml_content[ind]) - len(yaml_content[ind].lstrip()) == leading_spaces:
                insert_ind = ind
                break

        # Read env file
        f = open(env_path, 'r')
        env_content = f.readlines()
        f.close()

        # Prepare value pairs for yaml file
        value_pairs_list = [str(elem).replace("\n", "").split("=") for elem in env_content]
        final_set = HandyMix().flatten_nested_list(value_pairs_list)

        values_pairs = []
        for index in range(int(len(final_set) / 2)):
            name = (leading_spaces + 4) * ' ' + '- name: ' + str(final_set[2 * index]) + '\n'
            value = (leading_spaces + 6) * ' ' + 'value: "' + str(final_set[2 * index + 1]) + '"\n'

            values_pairs.append(name)
            values_pairs.append(value)
        values_pairs.insert(0, "        env:\n")

        # Build the yaml file
        new_yaml_file = ''.join(yaml_content[:insert_ind])
        new_yaml_file += ''.join(values_pairs)
        new_yaml_file += ''.join(yaml_content[insert_ind:])

        # Write env variables to yaml file
        f = open(yaml_path, "w")
        f.write(new_yaml_file)
        f.close()
