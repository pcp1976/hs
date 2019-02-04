from composer import Composer

# file_store(self, filepath: str, storage_type: str)
# file_retrieve(self, filepath: str, token: str)


def main():
    manager = Composer()
    manager.collect_plugins()
    manager.activate_plugins()
    secret = manager.pm.hook.crypto_encrypt(
        plaintext=manager.pm.hook.get_random_name()[0]
    )[0]
    manager.pm.hook.log_trace(plugin_name="__main__", message=secret)
    manager.pm.hook.log_notice(
        plugin_name="__main__",
        message=manager.pm.hook.crypto_decrypt(ciphertext=secret)[0],
    )
    manager.pm.hook.file_store(
        filepath="/home/paul/Documents/home server/README.md",
    )


if __name__ == "__main__":
    main()
